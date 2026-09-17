import frappe

TARGET_PARENT_DOCTYPE = "Journal Entry"


def sync_parent_field(doc, method=None):
    """Accounting Dimension insert/update par Journal Entry (parent) pe
    matching Custom Field auto create/update/unhide karo. Child-level
    (Journal Entry Account) fields ko touch nahi karta."""
    fieldname = doc.fieldname
    cf_name = frappe.db.get_value("Custom Field", {"dt": TARGET_PARENT_DOCTYPE, "fieldname": fieldname})

    if doc.disabled:
        if cf_name:
            cf = frappe.get_doc("Custom Field", cf_name)
            cf.hidden = 1
            cf.save(ignore_permissions=True)
            frappe.clear_cache(doctype=TARGET_PARENT_DOCTYPE)
        return

    if cf_name:
        cf = frappe.get_doc("Custom Field", cf_name)
        cf.label = doc.label
        cf.options = doc.document_type
        cf.hidden = 0
        cf.save(ignore_permissions=True)
    else:
        frappe.get_doc({
            "doctype": "Custom Field",
            "dt": TARGET_PARENT_DOCTYPE,
            "fieldname": fieldname,
            "label": doc.label,
            "fieldtype": "Link",
            "options": doc.document_type,
            "insert_after": "posting_date",
        }).insert(ignore_permissions=True)

    frappe.clear_cache(doctype=TARGET_PARENT_DOCTYPE)


def remove_parent_field(doc, method=None):
    """Accounting Dimension delete (on_trash) par parent field hide kar do
    (column drop nahi — data safe rehta hai)."""
    fieldname = doc.fieldname
    cf_name = frappe.db.get_value("Custom Field", {"dt": TARGET_PARENT_DOCTYPE, "fieldname": fieldname})
    if cf_name:
        cf = frappe.get_doc("Custom Field", cf_name)
        cf.hidden = 1
        cf.save(ignore_permissions=True)
        frappe.clear_cache(doctype=TARGET_PARENT_DOCTYPE)