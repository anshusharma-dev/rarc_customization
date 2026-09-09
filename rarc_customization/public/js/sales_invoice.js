frappe.ui.form.on('Sales Invoice', {
    profit_center: function(frm) {
        set_profit_center_in_child_tables(frm);
    }
});

frappe.ui.form.on('Sales Invoice Item', {
    items_add: function(frm, cdt, cdn) {
        if (frm.doc.profit_center) {
            frappe.model.set_value(cdt, cdn, 'profit_center', frm.doc.profit_center);
        }
    }
});

frappe.ui.form.on('Sales Taxes and Charges', {
    taxes_add: function(frm, cdt, cdn) {
        if (frm.doc.profit_center) {
            frappe.model.set_value(cdt, cdn, 'profit_center', frm.doc.profit_center);
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
