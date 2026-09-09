frappe.ui.form.on('Purchase Invoice', {
    onload: function(frm) {
        // Jab invoice load ho (naya ya existing), company check ho jaye
        set_itc_ineligible_if_trust(frm);
    },

    refresh: function(frm) {
        set_itc_ineligible_if_trust(frm);
    },

    profit_center: function(frm) {
        set_profit_center_in_child_tables(frm);
    },

    company: function(frm) {
        set_itc_ineligible_if_trust(frm);
    }
});

frappe.ui.form.on('Purchase Invoice Item', {
    items_add: function(frm, cdt, cdn) {
        let row = locals[cdt][cdn];

        // Profit center auto set
        if (frm.doc.profit_center) {
            frappe.model.set_value(cdt, cdn, 'profit_center', frm.doc.profit_center);
        }

        // Trust company hone par ITC ineligible auto set
        if (is_trust_company(frm.doc.company)) {
            frappe.model.set_value(cdt, cdn, 'is_ineligible_for_itc', 1);
        }
    }
});

frappe.ui.form.on('Purchase Taxes and Charges', {
    taxes_add: function(frm, cdt, cdn) {
        if (frm.doc.profit_center) {
            frappe.model.set_value(cdt, cdn, 'profit_center', frm.doc.profit_center);
        }
    }
});

// ---------- Helper Functions ----------

function set_profit_center_in_child_tables(frm) {
    if (!frm.doc.profit_center) return;

    (frm.doc.items || []).forEach(function (row) {
        row.profit_center = frm.doc.profit_center;
    });
    frm.refresh_field('items');

    (frm.doc.taxes || []).forEach(function (row) {
        row.profit_center = frm.doc.profit_center;
    });
    frm.refresh_field('taxes');
}

function is_trust_company(company) {
    if (!company) return false;
    return company.toLowerCase().includes('trust');
}

function set_itc_ineligible_if_trust(frm) {
    if (!frm.doc.items || !frm.doc.items.length) return;

    if (is_trust_company(frm.doc.company)) {
        let changed = false;
        frm.doc.items.forEach(function (row) {
            if (!row.is_ineligible_for_itc) {
                row.is_ineligible_for_itc = 1;
                changed = true;
            }
        });
        if (changed) {
            frm.refresh_field('items');
        }
    }
}