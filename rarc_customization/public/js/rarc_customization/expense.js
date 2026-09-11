frappe.provide("rarc_customization.utils");

rarc_customization.utils.filter_expense_account = function (frm) {
  if (frm.doc.custom_department) {
    frm.set_query("expense_account", "items", function () {
      return {
        query: "rarc_customization.customizations.department.api.get_coa.get_coa",
        filters: { custom_department: frm.doc.custom_department }
      };
    });
  }
};

rarc_customization.utils.set_expense_account = function (frm, cdt, cdn) {
  if (frm.doc.custom_department) {
    frappe.model.set_value(cdt, cdn, "expense_account", "");
  }
};