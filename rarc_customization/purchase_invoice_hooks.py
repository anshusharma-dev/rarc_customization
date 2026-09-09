import frappe


def set_profit_center_and_itc(doc, method=None):
    """
    Purchase Invoice ke validate/before_save par:
    1. Header ka profit_center child tables (items, taxes) me set karo
    2. Agar Company name me 'Trust' ho, to items me is_ineligible_for_itc = 1
    """

    # ---- 1. Profit Center propagate karo ----
    if doc.profit_center:
        for item in doc.items:
            if not item.profit_center:
                item.profit_center = doc.profit_center

        if hasattr(doc, "taxes"):
            for tax in doc.taxes:
                if not tax.profit_center:
                    tax.profit_center = doc.profit_center

    # ---- 2. Trust company check ----
    if doc.company and "trust" in doc.company.lower():
        for item in doc.items:
            item.is_ineligible_for_itc = 1
