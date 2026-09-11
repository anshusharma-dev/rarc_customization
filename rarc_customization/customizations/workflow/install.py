import frappe


def create_workflow_tracking_fields(doc, method=None):
	"""Hook: Workflow doctype's on_update. Ensures user_map exists on the target doctype
	whenever a workflow is made active — so this applies by default, no manual Customize Form."""
	if not doc.is_active or not doc.document_type:
		return

	if frappe.db.exists("Custom Field", {"dt": doc.document_type, "fieldname": "user_map"}):
		return

	frappe.get_doc({
		"doctype": "Custom Field",
		"dt": doc.document_type,
		"fieldname": "user_map",
		"label": "User Map",
		"fieldtype": "Small Text",
		"hidden": 1,
		"no_copy": 1,
		"allow_on_submit": 1,
		"insert_after": "workflow_state",
	}).insert(ignore_permissions=True)

	frappe.clear_cache(doctype=doc.document_type)