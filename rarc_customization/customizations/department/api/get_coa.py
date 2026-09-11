import frappe

@frappe.whitelist()
def get_coa(doctype, txt, searchfield, start, page_len, filters):
    department_id = filters.get("custom_department") if filters else None

    if department_id:
        coa_names = frappe.db.get_all(
            "Department COA",
            filters={"parent": department_id},
            fields=["chart_of_account"]
        )
        coa_list = [d["chart_of_account"] for d in coa_names]

        if not coa_list:
            return []

        accounts = frappe.db.get_all(
            "Account",
            filters={"name": ["in", coa_list], "root_type": "Expense", "is_group": 0},
            fields=["name", "account_name"]
        )
        return [(a["name"], a["account_name"]) for a in accounts]

    else:
        accounts = frappe.db.get_all(
            "Account",
            filters={"root_type": "Expense", "is_group": 0},
            fields=["name", "account_name"]
        )
        return [(a["name"], a["account_name"]) for a in accounts]