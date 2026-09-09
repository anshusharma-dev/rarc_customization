import frappe

from erpnext.accounts.report.tax_withholding_details import (
    tax_withholding_details as core_twd,
)

_original_execute = core_twd.execute


def execute_with_profit_center(filters=None):
    filters = filters or {}

    columns = [
        {
            "label": "Profit Center",
            "fieldname": "profit_center",
            "fieldtype": "Link",
            "options": "Profit Center",
            "width": 130,
        },
    ]

    # Agar zaroori filters (company/from_date/to_date) abhi tak set nahi hue,
    # to report ko force mat karo — empty result do
    if not filters.get("company") or not filters.get("from_date") or not filters.get("to_date"):
        return columns, []

    columns_from_core, data = _original_execute(filters)
    columns = columns_from_core + columns

    pi_names = {
        row.get("ref_no")
        for row in data
        if row.get("transaction_type") == "Purchase Invoice" and row.get("ref_no")
    }

    profit_center_map = {}
    if pi_names:
        pi_rows = frappe.get_all(
            "Purchase Invoice",
            filters={"name": ["in", list(pi_names)]},
            fields=["name", "profit_center"],
            limit_page_length=0,
        )
        profit_center_map = {pi.name: pi.profit_center for pi in pi_rows}

    for row in data:
        if row.get("transaction_type") == "Purchase Invoice":
            row["profit_center"] = profit_center_map.get(row.get("ref_no"))
        else:
            row["profit_center"] = None

    selected_profit_center = filters.get("profit_center")
    if selected_profit_center:
        data = [row for row in data if row.get("profit_center") == selected_profit_center]

    return columns, data


def apply_patch():
    core_twd.execute = execute_with_profit_center