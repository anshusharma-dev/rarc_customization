import frappe
from erpnext.stock.get_item_details import get_item_details


def set_item_tax_template(doc, method=None):
    """Auto-fetch item_tax_template for Sales/Purchase Invoice items —
    needed because Data Import bypasses the client-side item_code
    trigger that normally does this via the UI.
    Must run BEFORE other validate hooks that depend on tax data
    (e.g. tax_withholding), so this is registered first in the list."""

    for item in doc.items:
        if item.item_code and not item.item_tax_template:
            args = {
                "doctype": doc.doctype,
                "item_code": item.item_code,
                "company": doc.company,
                "customer": doc.get("customer"),
                "supplier": doc.get("supplier"),
                "tax_category": doc.get("tax_category"),
                "price_list": doc.get("selling_price_list") or doc.get("buying_price_list"),
                "currency": doc.currency,
                "conversion_rate": doc.conversion_rate,
                "transaction_date": doc.get("posting_date"),
                "name": item.name,
            }
            try:
                details = get_item_details(args, doc)
                if details.get("item_tax_template"):
                    item.item_tax_template = details.get("item_tax_template")
                    item.item_tax_rate = details.get("item_tax_rate")
            except Exception:
                frappe.log_error(
                    title=f"Item Tax Template fetch failed - {doc.doctype} - {doc.name}",
                    message=frappe.get_traceback(),
                )

    doc.set_missing_values()
    doc.calculate_taxes_and_totals()