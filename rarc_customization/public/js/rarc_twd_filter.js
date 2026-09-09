frappe.query_reports["Tax Withholding Details"] = frappe.query_reports["Tax Withholding Details"] || {};

console.log("[TWD Filter] Script loaded");

$.extend(frappe.query_reports["Tax Withholding Details"], {
    onload: function (report) {
        console.log("[TWD Filter] onload fired", report);

        function add_profit_center_filter() {
            if (report.get_filter("profit_center")) {
                console.log("[TWD Filter] profit_center already exists, skipping add");
                return;
            }

            console.log("[TWD Filter] Adding profit_center + profit_center_name fields");

            report.page.add_field({
                fieldname: "profit_center",
                label: __("Profit Center"),
                fieldtype: "Link",
                options: "Profit Center",
                change: function () {
                    var pc = report.get_filter_value("profit_center");
                    console.log("[TWD Filter] profit_center changed to:", pc);

                    if (pc) {
                        frappe.db.get_value("Profit Center", pc, "profit_center_name", function (r) {
                            console.log("[TWD Filter] Fetched profit_center_name:", r.profit_center_name);
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

            console.log("[TWD Filter] Fields added successfully");
        }

        add_profit_center_filter();

        const pageFormEl = report.page.wrapper.find(".page-form")[0];

        if (!pageFormEl) {
            console.warn("[TWD Filter] .page-form element not found, MutationObserver not attached");
        } else {
            console.log("[TWD Filter] Attaching MutationObserver to .page-form");

            const observer = new MutationObserver(function (mutations) {
                console.log("[TWD Filter] MutationObserver fired, mutation count:", mutations.length);

                if (!report.get_filter("profit_center")) {
                    console.warn("[TWD Filter] profit_center missing after mutation — re-adding");
                    add_profit_center_filter();
                } else {
                    console.log("[TWD Filter] profit_center still present, no action needed");
                }
            });

            observer.observe(pageFormEl, {
                childList: true,
                subtree: true,
            });

            console.log("[TWD Filter] MutationObserver attached");
        }
    }
});