frappe.after_ajax(function () {
    frappe.call({
        method: 'rarc_customization.customizations.workflow.api.workflow_action.get_active_workflow_doctypes',
        callback: function (r) {
            const doctypes = r.message || [];

            doctypes.forEach(function (dt) {
                frappe.ui.form.on(dt, {
                    refresh: function (frm) {
                        if (frm.doc.__islocal || !frm.doc.workflow_state) return;

                        frm.add_custom_button(__('Open Approval Dialog'), function () {
                            open_workflow_approval_dialog(frm);
                        });
                    }
                });
            });
        }
    });
});

function open_workflow_approval_dialog(frm) {
    frappe.call({
        method: 'rarc_customization.customizations.workflow.api.workflow_action.get_unique_roles_with_users',
        args: {
            doctype: frm.doc.doctype,
            docname: frm.doc.name
        },
        callback: function (r) {
            const rows = r.message || [];

            const dialog = new frappe.ui.Dialog({
                title: __('Approval Status'),
                fields: [
                    {
                        fieldname: 'approval_table',
                        fieldtype: 'Table',
                        cannot_add_rows: true,
                        in_place_edit: false,
                        data: rows.map(function (row) {
                            return {
                                role: row.role,
                                user: Array.isArray(row.user) ? row.user.join(', ') : row.user,
                                delegated_user: row.delegated_user || '',
                                action: row.action || '',
                                approve_at: row.approve_at || '',
                                remarks: row.remarks || ''
                            };
                        }),
                        fields: [
                            { fieldname: 'role', fieldtype: 'Link', options: 'Role', label: __('Role'), in_list_view: 1, read_only: 1 },
                            { fieldname: 'user', fieldtype: 'Data', label: __('User'), in_list_view: 1, read_only: 1 },
                            { fieldname: 'delegated_user', fieldtype: 'Data', label: __('Delegated User'), in_list_view: 1, read_only: 1 },
                            { fieldname: 'action', fieldtype: 'Data', label: __('Action Taken'), in_list_view: 1, read_only: 1 },
                            { fieldname: 'approve_at', fieldtype: 'Data', label: __('Action Taken At'), in_list_view: 1, read_only: 1 },
                            { fieldname: 'remarks', fieldtype: 'Data', label: __('Remarks'), in_list_view: 1, read_only: 1 }
                        ]
                    }
                ],
                primary_action_label: __('Close'),
                primary_action: function () {
                    dialog.hide();
                }
            });

            dialog.show();
        }
    });
}