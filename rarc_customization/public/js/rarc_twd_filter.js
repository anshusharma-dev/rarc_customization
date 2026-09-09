$(document).on("page-change", function () {
    setTimeout(function () {
        if (
            !frappe.query_report ||
            frappe.query_report.report_name !== "Tax Withholding Details"
        ) {
            return;
        }

        if (frappe.query_report._profit_center_filter_added) {
            return;
        }

        frappe.query_report.page.add_field({
            fieldname: "profit_center",
            label: __("Profit Center"),
            fieldtype: "Link",
            options: "Profit Center",
            change: function () {
                var pc = frappe.query_report.get_filter_value("profit_center");

                if (pc) {
                    frappe.db.get_value("Profit Center", pc, "profit_center_name", function (r) {
                        frappe.query_report.set_filter_value("profit_center_name", r.profit_center_name || "");
                        frappe.query_report.refresh();
                    });
                } else {
                    frappe.query_report.set_filter_value("profit_center_name", "");
                    frappe.query_report.refresh();
                }
            }
        });

        frappe.query_report.page.add_field({
            fieldname: "profit_center_name",
            label: __("Profit Center Name"),
            fieldtype: "Data",
            read_only: 1,
        });

        frappe.query_report._profit_center_filter_added = true;
    }, 500);
});
