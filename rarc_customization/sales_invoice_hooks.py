import frappe


def set_profit_center_in_child_tables(doc, method=None):
    if doc.profit_center:
        for item in doc.items:
            if not item.profit_center:
                item.profit_center = doc.profit_center

        if hasattr(doc, "taxes"):
            for tax in doc.taxes:
                if not tax.profit_center:
                    tax.profit_center = doc.profit_center

    if doc.cost_center:
        for item in doc.items:
            if not item.cost_center:
                item.cost_center = doc.cost_center

        if hasattr(doc, "taxes"):
            for tax in doc.taxes:
                if not tax.cost_center:
                    tax.cost_center = doc.cost_center

    if doc.business_place:
        for item in doc.items:
            if not item.business_place:
                item.business_place = doc.business_place

        if hasattr(doc, "taxes"):
            for tax in doc.taxes:
                if not tax.business_place:
                    tax.business_place = doc.business_place

    if doc.project:
        for item in doc.items:
            if not item.project:
                item.project = doc.project

        if hasattr(doc, "taxes"):
            for tax in doc.taxes:
                if not tax.project:
                    tax.project = doc.project