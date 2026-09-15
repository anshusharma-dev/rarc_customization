import frappe
from erpnext.accounts.doctype.tax_withholding_category.tax_withholding_category import (
    get_party_tax_withholding_details,
)


def set_item_wise_tax_withholding(doc, method=None):
    tds_items = [item for item in doc.items if item.get("custom_apply_tds")]
    if not tds_items:
        return

    category = frappe.db.get_value("Customer", doc.customer, "tax_withholding_category")
    if not category:
        return

    doc.taxes = [t for t in doc.taxes if not t.get("is_tax_withholding_account")]
    doc.custom_tax_withholding_entries = []

    tds_items_amount = sum(item.amount for item in tds_items)
    non_tds_items_amount = doc.net_total - tds_items_amount

    original_grand_total = doc.grand_total
    doc.grand_total = doc.grand_total - non_tds_items_amount

    try:
        tax_row = get_party_tax_withholding_details(doc, category)
    finally:
        doc.grand_total = original_grand_total

    if not tax_row or not tax_row.get("tax_amount"):
        return

    doc.append("taxes", tax_row)

    for item in tds_items:
        item_share = (item.amount / tds_items_amount) * tax_row["tax_amount"]
        doc.append("custom_tax_withholding_entries", {
            "item_row": item.name,
            "item_code": item.item_code,
            "party_type": "Customer",
            "party": doc.customer,
            "tax_withholding_category": category,
            "taxable_amount": item.amount,
            "tax_rate": tax_row.get("rate"),
            "withholding_amount": item_share,
            "taxable_doctype": "Sales Invoice",
            "taxable_name": doc.name,
            "taxable_date": doc.posting_date,
            "withholding_doctype": "Sales Invoice",
            "withholding_name": doc.name,
            "withholding_date": doc.posting_date,
            "conversion_rate": doc.conversion_rate or 1,
            "status": "Settled" if doc.docstatus == 1 else "Draft",
        })

    doc.calculate_taxes_and_totals()