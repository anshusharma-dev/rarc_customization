frappe.ui.form.on('Journal Entry', {
    refresh: function(frm) {
        if (frm.doc.docstatus !== 1) return;

        let current_user = frappe.session.user;
        let is_owner = frm.doc.owner === current_user;
        let is_admin = current_user === "Administrator";

        if (is_owner || is_admin) return;

        // Observe the Actions dropdown menu so we can remove the
        // "Reverse Journal Entry" button as soon as any app re-adds it
        let $actions_menu = frm.page.wrapper.find('.actions-btn-group .dropdown-menu');
        if (!$actions_menu.length) return;

        let observer = new MutationObserver(function() {
            frm.remove_custom_button('Reverse Journal Entry', 'Actions');
        });

        observer.observe($actions_menu[0], { childList: true, subtree: true });

        // Try once immediately as well, in case it's already added
        frm.remove_custom_button('Reverse Journal Entry', 'Actions');

        // Disconnect observer when navigating away from the form (avoid memory leak)
        frm.page.wrapper.on('hide', () => observer.disconnect());
    },

    profit_center: function(frm) {
        // Skip if this change itself came from the row -> parent sync below
        if (frm.__syncing_dimension) return;
        force_apply_parent_dimension(frm, "profit_center");
    },

    business_place: function(frm) {
        if (frm.__syncing_dimension) return;
        force_apply_parent_dimension(frm, "business_place");
    },

    accounts_add: function(frm, cdt, cdn) {
        // New empty row added -> just fill it with the parent's current value
        let row = locals[cdt][cdn];
        ["profit_center", "business_place"].forEach(function(fieldname) {
            if (frm.doc[fieldname] && !row[fieldname]) {
                frappe.model.set_value(cdt, cdn, fieldname, frm.doc[fieldname]);
            }
        });
    },

    accounts_remove: function(frm) {
        // A row was removed -> re-check if remaining rows are now all equal
        check_and_sync_parent_from_rows(frm, "profit_center");
        check_and_sync_parent_from_rows(frm, "business_place");
    }
});

frappe.ui.form.on('Journal Entry Account', {
    profit_center: function(frm, cdt, cdn) {
        check_and_sync_parent_from_rows(frm, "profit_center");
    },
    business_place: function(frm, cdt, cdn) {
        check_and_sync_parent_from_rows(frm, "business_place");
    }
});

function force_apply_parent_dimension(frm, fieldname) {
    // Parent field set/changed -> overwrite this dimension in every row,
    // regardless of the row's existing value.
    // If parent field is cleared, rows are left untouched (not cleared).
    if (!frm.doc[fieldname]) return;

    (frm.doc.accounts || []).forEach(function(row) {
        frappe.model.set_value(row.doctype, row.name, fieldname, frm.doc[fieldname]);
    });
}

function check_and_sync_parent_from_rows(frm, fieldname) {
    // If every row has the same non-empty value for this dimension,
    // auto-fill the parent field with that value.
    // If values differ across rows, the parent field is left as-is.
    let rows = frm.doc.accounts || [];
    if (!rows.length) return;

    let values = rows.map(function(row) { return row[fieldname]; });
    let first = values[0];
    let all_same = values.every(function(v) { return v === first; });

    if (all_same && first && frm.doc[fieldname] !== first) {
        // Hold the guard flag until set_value's own change-trigger has
        // actually fired, since set_value is asynchronous
        frm.__syncing_dimension = true;
        frm.set_value(fieldname, first).then(function() {
            frm.__syncing_dimension = false;
        });
    }
}
