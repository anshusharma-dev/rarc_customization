import json

import frappe
from frappe.utils import now_datetime
from frappe.workflow.doctype.workflow_action.workflow_action import (
	get_next_possible_transitions,
)


def _get_active_workflow_name(doctype):
	return frappe.db.get_value("Workflow", {"document_type": doctype, "is_active": 1}, "name")


def _get_valid_transition(doc, old_state, new_state):
	workflow_name = _get_active_workflow_name(doc.doctype)
	if not workflow_name:
		return None

	transitions = frappe.db.get_all(
		"Workflow Transition",
		filters={"parent": workflow_name, "state": old_state, "next_state": new_state},
		fields=["allowed", "action", "condition"],
	)

	for t in transitions:
		if t.condition:
			try:
				if not frappe.safe_eval(t.condition, None, {"doc": doc, "frappe": frappe}):
					continue
			except Exception:
				frappe.log_error(
					title="Workflow transition condition eval failed",
					message=frappe.get_traceback(),
				)
				continue
		return t

	return None


def track_state_user(doc, method=None):
	"""doc_event hook — wire to on_update of workflow-enabled doctypes (e.g. Purchase Invoice)."""
	if not doc.meta.has_field("workflow_state") or not doc.meta.has_field("user_map"):
		return

	old_doc = doc.get_doc_before_save()
	old_state = old_doc.workflow_state if old_doc else None
	new_state = doc.workflow_state

	if not new_state or old_state == new_state:
		return

	transition = _get_valid_transition(doc, old_state, new_state)
	if not transition:
		return

	state_log = {}
	if doc.user_map:
		try:
			state_log = json.loads(doc.user_map)
		except (TypeError, ValueError):
			state_log = {}

	state_log[transition.allowed] = {
		"name": frappe.session.user,
		"action": transition.action,
		"last_comment_reason": None,
		"modified_on": now_datetime().strftime("%d-%m-%Y %H:%M"),
	}

	frappe.db.set_value(doc.doctype, doc.name, "user_map", json.dumps(state_log, indent=2))


def get_unique_roles_with_users(doctype, docname):
	doc = frappe.get_doc(doctype, docname)
	if not doc.meta.has_field("workflow_state"):
		frappe.throw(f"{doctype} does not have workflow_state")

	workflow_name = _get_active_workflow_name(doctype)
	if not workflow_name:
		frappe.throw(f"No active workflow found for {doctype}")

	transitions = frappe.db.get_all(
		"Workflow Transition",
		filters={"parent": workflow_name},
		fields=["state", "next_state", "allowed", "condition", "action"],
		order_by="idx",
	)

	state_log = {}
	if doc.get("user_map"):
		try:
			state_log = json.loads(doc.user_map)
		except (TypeError, ValueError):
			state_log = {}

	next_transitions = get_next_possible_transitions(workflow_name, doc.workflow_state, doc)
	next_states = {t.next_state for t in next_transitions} if next_transitions else set()

	processed_roles = set()
	rows = []

	for t in transitions:
		if t.allowed in processed_roles:
			continue

		if t.condition:
			try:
				if not frappe.safe_eval(t.condition, None, {"doc": doc, "frappe": frappe}):
					continue
			except Exception:
				continue

		if t.allowed in state_log:
			entry = state_log[t.allowed]
			rows.append({
				"role": t.allowed,
				"user": entry.get("name"),
				"delegated_user": None,
				"action": entry.get("action"),
				"approve_at": entry.get("modified_on"),
				"remarks": entry.get("last_comment_reason"),
			})
			processed_roles.add(t.allowed)
			continue

		if not next_states:
			continue

		if t.state != doc.workflow_state and t.next_state not in next_states:
			continue

		users_with_role = frappe.db.get_list(
			"Has Role", filters={"role": t.allowed, "parenttype": "User"}, pluck="parent"
		)
		eligible_users = [
			u for u in users_with_role if frappe.has_permission(doctype, "write", doc=doc, user=u)
		]

		rows.append({
			"role": t.allowed,
			"user": eligible_users,
			"delegated_user": None,
			"action": None,
			"approve_at": None,
			"remarks": None,
		})
		processed_roles.add(t.allowed)

	return rows