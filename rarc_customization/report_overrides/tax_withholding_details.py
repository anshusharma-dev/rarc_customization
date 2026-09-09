import frappe
from frappe.utils import nowdate, get_first_day

from erpnext.accounts.report.tax_withholding_details import (
    tax_withholding_details as core_twd,
)

_original_execute = core_twd.execute


def execute_with_profit_center(filters=None):
    filters = filters or {}

    # Defensive default: agar from_date/to_date missing hain, to safe defaults set karo
    if not filters.get("from_date") or not filters.get("to_date"):
        filters["from_date"] = filters.get("from_date") or get_first_day(nowdate())
        filters["to_date"] = filters.get("to_date") or nowdate()

    columns, data = _original_execute(filters)

    columns.extend([
        {
            "label": "Profit Center",
            "fieldname": "profit_center",
            "fieldtype": "Link",
            "options": "Profit Center",
            "width": 130,
        },
        {
            "label": "Profit Center Name",
            "fieldname": "profit_center_name",
            "fieldtype": "Data",
            "width": 150,
        },
    ])

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

    profit_center_ids = {pc for pc in profit_center_map.values() if pc}

    profit_center_name_map = {}
    if profit_center_ids:
        pc_rows = frappe.get_all(
            "Profit Center",
            filters={"name": ["in", list(profit_center_ids)]},
            fields=["name", "profit_center_name"],
            limit_page_length=0,
        )
        profit_center_name_map = {pc.name: pc.profit_center_name for pc in pc_rows}

    for row in data:
        if row.get("transaction_type") == "Purchase Invoice":
            pc = profit_center_map.get(row.get("ref_no"))
            row["profit_center"] = pc
            row["profit_center_name"] = profit_center_name_map.get(pc) if pc else None
        else:
            row["profit_center"] = None
            row["profit_center_name"] = None

    selected_profit_center = filters.get("profit_center")
    if selected_profit_center:
        data = [row for row in data if row.get("profit_center") == selected_profit_center]

    return columns, data


def apply_patch():
    core_twd.execute = execute_with_profit_center