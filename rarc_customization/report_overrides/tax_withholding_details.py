import frappe

from erpnext.accounts.report.tax_withholding_details import (
    tax_withholding_details as core_twd,
)


print("========== TAX WITHHOLDING PATCH FILE LOADED ==========")


# Keep original ERPNext execute function
_original_execute = core_twd.execute

print(
    "TAX WITHHOLDING ORIGINAL EXECUTE:",
    _original_execute,
)


def execute_with_profit_center(filters=None):

    print("\n")
    print("========================================================")
    print("TAX WITHHOLDING CUSTOM EXECUTE STARTED")
    print("========================================================")

    try:
        filters = filters or {}

        print("TAX WITHHOLDING FILTERS:")
        print(frappe.as_json(filters))

        # ---------------------------------------------------------
        # Run original ERPNext report
        # ---------------------------------------------------------

        print("CALLING ORIGINAL TAX WITHHOLDING EXECUTE...")

        columns, data = _original_execute(filters)

        print("ORIGINAL EXECUTE COMPLETED")

        print("COLUMN COUNT:", len(columns))
        print("DATA ROW COUNT:", len(data))

        # ---------------------------------------------------------
        # Debug original columns
        # ---------------------------------------------------------

        print("\n---------- ORIGINAL COLUMNS ----------")

        for column in columns:
            print(column)

        # ---------------------------------------------------------
        # Debug original data
        # ---------------------------------------------------------

        print("\n---------- ORIGINAL DATA ----------")

        for index, row in enumerate(data):

            print(
                "ROW",
                index,
                ":",
                frappe.as_json(row)
            )

        # ---------------------------------------------------------
        # Add Profit Center columns
        # ---------------------------------------------------------

        print("\nADDING PROFIT CENTER COLUMNS...")

        columns.extend(
            [
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
            ]
        )

        print("PROFIT CENTER COLUMNS ADDED")

        # ---------------------------------------------------------
        # Collect Purchase Invoice names
        # ---------------------------------------------------------

        print("\n---------- COLLECTING PURCHASE INVOICES ----------")

        pi_names = set()

        for index, row in enumerate(data):

            transaction_type = row.get("transaction_type")
            ref_no = row.get("ref_no")

            print(
                f"ROW {index} -> "
                f"transaction_type={transaction_type}, "
                f"ref_no={ref_no}"
            )

            if (
                transaction_type == "Purchase Invoice"
                and ref_no
            ):
                pi_names.add(ref_no)

        print("PURCHASE INVOICE NAMES FOUND:")
        print(frappe.as_json(list(pi_names)))

        print("PURCHASE INVOICE COUNT:", len(pi_names))

        # ---------------------------------------------------------
        # Get Profit Center from Purchase Invoice
        # ---------------------------------------------------------

        profit_center_map = {}

        if pi_names:

            print("\nFETCHING PURCHASE INVOICES...")

            pi_rows = frappe.get_all(
                "Purchase Invoice",
                filters={
                    "name": ["in", list(pi_names)]
                },
                fields=[
                    "name",
                    "profit_center",
                ],
                limit_page_length=0,
            )

            print(
                "PURCHASE INVOICE RECORDS FETCHED:",
                len(pi_rows)
            )

            for pi in pi_rows:

                print(
                    "PI:",
                    pi.name,
                    "=> PROFIT CENTER:",
                    pi.profit_center
                )

                profit_center_map[pi.name] = pi.profit_center

        else:

            print(
                "WARNING: NO PURCHASE INVOICE NAMES FOUND!"
            )

        print("\nPROFIT CENTER MAP:")
        print(frappe.as_json(profit_center_map))

        # ---------------------------------------------------------
        # Collect Profit Centers
        # ---------------------------------------------------------

        profit_center_ids = {
            profit_center
            for profit_center in profit_center_map.values()
            if profit_center
        }

        print("\nPROFIT CENTER IDS:")
        print(frappe.as_json(list(profit_center_ids)))

        print(
            "PROFIT CENTER COUNT:",
            len(profit_center_ids)
        )

        # ---------------------------------------------------------
        # Get Profit Center Names
        # ---------------------------------------------------------

        profit_center_name_map = {}

        if profit_center_ids:

            print("\nFETCHING PROFIT CENTER RECORDS...")

            pc_rows = frappe.get_all(
                "Profit Center",
                filters={
                    "name": ["in", list(profit_center_ids)]
                },
                fields=[
                    "name",
                    "profit_center_name",
                ],
                limit_page_length=0,
            )

            print(
                "PROFIT CENTER RECORDS FETCHED:",
                len(pc_rows)
            )

            for pc in pc_rows:

                print(
                    "PROFIT CENTER:",
                    pc.name,
                    "=> NAME:",
                    pc.profit_center_name
                )

                profit_center_name_map[
                    pc.name
                ] = pc.profit_center_name

        else:

            print(
                "WARNING: NO PROFIT CENTER IDS FOUND!"
            )

        print("\nPROFIT CENTER NAME MAP:")
        print(frappe.as_json(profit_center_name_map))

        # ---------------------------------------------------------
        # Add Profit Center values to rows
        # ---------------------------------------------------------

        print("\n---------- ADDING PROFIT CENTER TO ROWS ----------")

        for index, row in enumerate(data):

            transaction_type = row.get("transaction_type")
            ref_no = row.get("ref_no")

            print(
                f"PROCESSING ROW {index}: "
                f"transaction_type={transaction_type}, "
                f"ref_no={ref_no}"
            )

            if transaction_type == "Purchase Invoice":

                profit_center = profit_center_map.get(ref_no)

                print(
                    f"ROW {index} PROFIT CENTER:",
                    profit_center
                )

                row["profit_center"] = profit_center

                if profit_center:

                    profit_center_name = (
                        profit_center_name_map.get(
                            profit_center
                        )
                    )

                    print(
                        f"ROW {index} PROFIT CENTER NAME:",
                        profit_center_name
                    )

                    row["profit_center_name"] = (
                        profit_center_name
                    )

                else:

                    print(
                        f"ROW {index}: "
                        "NO PROFIT CENTER FOUND"
                    )

                    row["profit_center_name"] = None

            else:

                print(
                    f"ROW {index}: "
                    "NOT A PURCHASE INVOICE"
                )

                row["profit_center"] = None
                row["profit_center_name"] = None

        # ---------------------------------------------------------
        # Debug final data before filter
        # ---------------------------------------------------------

        print("\n---------- DATA BEFORE PROFIT CENTER FILTER ----------")

        for index, row in enumerate(data):

            print(
                f"ROW {index}: "
                f"ref_no={row.get('ref_no')}, "
                f"transaction_type={row.get('transaction_type')}, "
                f"profit_center={row.get('profit_center')}, "
                f"profit_center_name={row.get('profit_center_name')}"
            )

        # ---------------------------------------------------------
        # Profit Center Filter
        # ---------------------------------------------------------

        selected_profit_center = filters.get(
            "profit_center"
        )

        print("\nSELECTED PROFIT CENTER FILTER:")
        print(selected_profit_center)

        if selected_profit_center:

            old_count = len(data)

            data = [
                row
                for row in data
                if row.get("profit_center")
                == selected_profit_center
            ]

            print(
                "PROFIT CENTER FILTER APPLIED"
            )

            print(
                "ROWS BEFORE FILTER:",
                old_count
            )

            print(
                "ROWS AFTER FILTER:",
                len(data)
            )

        else:

            print(
                "NO PROFIT CENTER FILTER APPLIED"
            )

        # ---------------------------------------------------------
        # Final debug
        # ---------------------------------------------------------

        print("\n---------- FINAL DATA ----------")

        for index, row in enumerate(data):

            print(
                f"FINAL ROW {index}:",
                frappe.as_json(row)
            )

        print("\nFINAL COLUMN COUNT:", len(columns))
        print("FINAL DATA COUNT:", len(data))

        print("\n========================================================")
        print("TAX WITHHOLDING CUSTOM EXECUTE FINISHED")
        print("========================================================")

        return columns, data

    except Exception:

        print(
            "\n!!!!!!!! TAX WITHHOLDING PATCH ERROR !!!!!!!!"
        )

        print(
            frappe.get_traceback()
        )

        frappe.log_error(
            frappe.get_traceback(),
            "Tax Withholding Profit Center Patch Error",
        )

        raise


# -------------------------------------------------------------
# Apply Monkey Patch
# -------------------------------------------------------------

def apply_patch():

    print(
        "\n========== APPLYING TAX WITHHOLDING PATCH =========="
    )

    print(
        "BEFORE PATCH EXECUTE:",
        core_twd.execute
    )

    core_twd.execute = execute_with_profit_center

    print(
        "AFTER PATCH EXECUTE:",
        core_twd.execute
    )

    print(
        "PATCH APPLIED SUCCESSFULLY"
    )


# IMPORTANT
apply_patch()

print(
    "========== TAX WITHHOLDING PATCH READY =========="
)

