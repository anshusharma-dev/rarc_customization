import frappe


def set_profit_center_in_child_tables(doc, method=None):
    """
    Sales Invoice ke validate par:
    Header ka profit_center child tables (items, taxes) me set karo
    """

    if not doc.profit_center:
        return

    for item in doc.items:
        if not item.profit_center:
            item.profit_center = doc.profit_center

    if hasattr(doc, "taxes"):
        for tax in doc.taxes:
            if not tax.profit_center:
                tax.profit_center = doc.profit_center
