frappe.ui.form.on('Material Request', {
    onload_post_render: function(frm) {
        rarc_customization.utils.filter_expense_account(frm);
    },

    custom_department: function(frm) {
        rarc_customization.utils.filter_expense_account(frm);
    }
});

frappe.ui.form.on('Material Request Item', {
    item_code: function(frm, cdt, cdn) {
        setTimeout(() => {
            rarc_customization.utils.set_expense_account(frm, cdt, cdn);
            rarc_customization.utils.filter_expense_account(frm);
        }, 1000);
    }
});