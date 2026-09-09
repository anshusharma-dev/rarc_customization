frappe.query_reports["Tax Withholding Details"] = frappe.query_reports["Tax Withholding Details"] || {};

$.extend(frappe.query_reports["Tax Withholding Details"], {
    onload: function (report) {
        function add_profit_center_filter() {
            if (report.get_filter("profit_center")) return;

            report.page.add_field({
                fieldname: "profit_center",
                label: __("Profit Center"),
                fieldtype: "Link",
                options: "Profit Center",
                change: function () {
                    report.refresh();
                }
            });
        }

        add_profit_center_filter();

        const pageFormEl = report.page.wrapper.find(".page-form")[0];

        if (pageFormEl) {
            const observer = new MutationObserver(function () {
                if (!report.get_filter("profit_center")) {
                    add_profit_center_filter();
                }
            });

            observer.observe(pageFormEl, {
                childList: true,
                subtree: true,
            });
        }
    }
});