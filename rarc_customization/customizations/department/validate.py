import frappe

def validate_department_gl(doc, method):
    if not doc.get("custom_department"):
        return

    allowed = frappe.db.get_all(
        "Department COA",
        filters={"parent": doc.custom_department},
        pluck="chart_of_account"
    )

    if not allowed:
        return  # koi mapping hi nahi, to validation skip (ya chaho to yahan bhi block kar sakte ho)

    for item in doc.items:
        if item.expense_account and item.expense_account not in allowed:
            frappe.throw(
                f"Row #{item.idx}: Expense Account <b>{item.expense_account}</b> is not mapped to Department <b>{doc.custom_department}</b>"
            )