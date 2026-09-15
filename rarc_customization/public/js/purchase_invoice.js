frappe.ui.form.on('Purchase Invoice', {
    onload: function(frm) {
        // Jab invoice load ho (naya ya existing), company check ho jaye
        set_itc_ineligible_if_trust(frm);
    },

    onload_post_render: function(frm) {
        rarc_customization.utils.filter_expense_account(frm);
    },

    refresh: function(frm) {
        set_itc_ineligible_if_trust(frm);
    },

    profit_center: function(frm) {
        set_profit_center_in_child_tables(frm);
    },

    cost_center: function(frm) {
        set_cost_center_in_child_tables(frm);
    },

    business_place: function(frm) {
        set_business_place_in_child_tables(frm);
    },

    company: function(frm) {
        set_itc_ineligible_if_trust(frm);
    },

    custom_department: function(frm) {
        rarc_customization.utils.filter_expense_account(frm);
    }
});

frappe.ui.form.on('Purchase Invoice Item', {
    items_add: function(frm, cdt, cdn) {
        let row = locals[cdt][cdn];

        // Profit center auto set
        if (frm.doc.profit_center) {
            frappe.model.set_value(cdt, cdn, 'profit_center', frm.doc.profit_center);
        }

        // Cost center auto set
        if (frm.doc.cost_center) {
            frappe.model.set_value(cdt, cdn, 'cost_center', frm.doc.cost_center);
        }

        // Business place auto set
        if (frm.doc.business_place) {
            frappe.model.set_value(cdt, cdn, 'business_place', frm.doc.business_place);
        }

        // Trust company hone par ITC ineligible auto set
        if (is_trust_company(frm.doc.company)) {
            frappe.model.set_value(cdt, cdn, 'is_ineligible_for_itc', 1);
        }
    },

    item_code: function(frm, cdt, cdn) {
        setTimeout(() => {
            rarc_customization.utils.set_expense_account(frm, cdt, cdn);
            rarc_customization.utils.filter_expense_account(frm);
        }, 1000);
    }
});

frappe.ui.form.on('Purchase Taxes and Charges', {
    taxes_add: function(frm, cdt, cdn) {
        if (frm.doc.profit_center) {
            frappe.model.set_value(cdt, cdn, 'profit_center', frm.doc.profit_center);
        }
        if (frm.doc.cost_center) {
            frappe.model.set_value(cdt, cdn, 'cost_center', frm.doc.cost_center);
        }
        if (frm.doc.business_place) {
            frappe.model.set_value(cdt, cdn, 'business_place', frm.doc.business_place);
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

function set_cost_center_in_child_tables(frm) {
    if (!frm.doc.cost_center) return;

    (frm.doc.items || []).forEach(function (row) {
        row.cost_center = frm.doc.cost_center;
    });
    frm.refresh_field('items');

    (frm.doc.taxes || []).forEach(function (row) {
        row.cost_center = frm.doc.cost_center;
    });
    frm.refresh_field('taxes');
}

function set_business_place_in_child_tables(frm) {
    if (!frm.doc.business_place) return;

    (frm.doc.items || []).forEach(function (row) {
        row.business_place = frm.doc.business_place;
    });
    frm.refresh_field('items');

    (frm.doc.taxes || []).forEach(function (row) {
        row.business_place = frm.doc.business_place;
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