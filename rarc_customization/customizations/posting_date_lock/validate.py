import frappe


def preserve_posting_date(doc, method):
    """
    If the 'Edit Posting Date and Time' checkbox (set_posting_time) is unchecked,
    prevent the posting_date/time from changing on an existing document —
    this overrides the core controller's default reset-to-today behavior.
    """
    if doc.get("set_posting_time"):
        return  # user explicitly ticked the checkbox, allow the change

    if doc.is_new():
        return  # new document — current date/time is expected

    original = frappe.db.get_value(
        doc.doctype, doc.name, ["posting_date", "posting_time"], as_dict=True
    )

    if original and original.posting_date:
        doc.posting_date = original.posting_date
        doc.posting_time = original.posting_time