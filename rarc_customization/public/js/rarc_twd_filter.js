frappe.query_reports["Tax Withholding Details"] = frappe.query_reports["Tax Withholding Details"] || {};

$.extend(frappe.query_reports["Tax Withholding Details"], {
    onload: function (report) {
        report.page.add_field({
            fieldname: "profit_center",
            label: __("Profit Center"),
            fieldtype: "Link",
            options: "Profit Center",
            change: function () {
                var pc = report.get_filter_value("profit_center");

                if (pc) {
                    frappe.db.get_value("Profit Center", pc, "profit_center_name", function (r) {
                        report.set_filter_value("profit_center_name", r.profit_center_name || "");
                        report.refresh();
                    });
                } else {
                    report.set_filter_value("profit_center_name", "");
                    report.refresh();
                }
            }
        });

        report.page.add_field({
            fieldname: "profit_center_name",
            label: __("Profit Center Name"),
            fieldtype: "Data",
            read_only: 1,
        });
    }
});