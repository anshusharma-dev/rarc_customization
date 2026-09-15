frappe.ui.form.on('Sales Invoice', {
    profit_center: function(frm) {
        set_profit_center_in_child_tables(frm);
    },

    cost_center: function(frm) {
        set_cost_center_in_child_tables(frm);
    },

    business_place: function(frm) {
        set_business_place_in_child_tables(frm);
    },

    project: function(frm) {
        set_project_in_child_tables(frm);
    }
});

frappe.ui.form.on('Sales Invoice Item', {
    items_add: function(frm, cdt, cdn) {
        if (frm.doc.profit_center) {
            frappe.model.set_value(cdt, cdn, 'profit_center', frm.doc.profit_center);
        }
        if (frm.doc.cost_center) {
            frappe.model.set_value(cdt, cdn, 'cost_center', frm.doc.cost_center);
        }
        if (frm.doc.business_place) {
            frappe.model.set_value(cdt, cdn, 'business_place', frm.doc.business_place);
        }
        if (frm.doc.project) {
            frappe.model.set_value(cdt, cdn, 'project', frm.doc.project);
        }
    }
});

frappe.ui.form.on('Sales Taxes and Charges', {
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
        if (frm.doc.project) {
            frappe.model.set_value(cdt, cdn, 'project', frm.doc.project);
        }
    }
});

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

function set_project_in_child_tables(frm) {
    if (!frm.doc.project) return;

    (frm.doc.items || []).forEach(function (row) {
        row.project = frm.doc.project;
    });
    frm.refresh_field('items');

    (frm.doc.taxes || []).forEach(function (row) {
        row.project = frm.doc.project;
    });
    frm.refresh_field('taxes');
}