console.log("[file_list.js] SCRIPT LOADED - version DEBUG-7 (menu inject via route watch)");

function inject_zip_action() {
    if (typeof cur_list === 'undefined' || !cur_list || !cur_list.page) {
        return;
    }

    // Already added? check a flag on page object
    if (cur_list.page.rarc_zip_action_added) {
        return;
    }
    cur_list.page.rarc_zip_action_added = true;

    const export_zip_action = function () {
        console.log("[file_list.js] 'Download as ZIP (Grouped)' clicked");

        let selected = cur_list.get_checked_items().map(d => d.name);
        console.log("[file_list.js] Selected file docnames:", selected);

        if (!selected.length) {
            frappe.msgprint(__('Please select at least one file'));
            return;
        }

        let params = encodeURIComponent(JSON.stringify(selected));
        let cache_buster = new Date().getTime();
        let url = `/api/method/rarc_customization.api.zip_files?files=${params}&_=${cache_buster}`;

        console.log("[file_list.js] Final request URL:", url);
        window.location.href = url;
    };

    cur_list.page.add_action_item(__('Download as ZIP (Grouped)'), export_zip_action);
    console.log("[file_list.js] 'Download as ZIP (Grouped)' added to Actions menu");
}

setInterval(function () {
    const route = frappe.get_route ? frappe.get_route() : [];
    const is_file_list = route[0] === 'List' && route[1] === 'File';

    if (is_file_list) {
        inject_zip_action();
    }
}, 1000);

console.log("[file_list.js] Route watcher for Actions menu injection started");