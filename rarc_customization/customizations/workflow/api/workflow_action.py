import frappe

from rarc_customization.customizations.workflow.workflow_timeline import (
	get_unique_roles_with_users as _get_unique_roles_with_users,
)


@frappe.whitelist()
def get_active_workflow_doctypes():
	return frappe.db.get_list("Workflow", filters={"is_active": 1}, pluck="document_type", distinct=True)


@frappe.whitelist()
def get_unique_roles_with_users(doctype, docname):
	return _get_unique_roles_with_users(doctype, docname)