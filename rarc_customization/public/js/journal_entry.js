frappe.ui.form.on('Journal Entry', {
    refresh: function(frm) {
        if (frm.doc.docstatus !== 1) return;

        let current_user = frappe.session.user;
        let is_owner = frm.doc.owner === current_user;
        let is_admin = current_user === "Administrator";

        if (is_owner || is_admin) return;

        // Actions dropdown menu ko observe karo
        let $actions_menu = frm.page.wrapper.find('.actions-btn-group .dropdown-menu');
        if (!$actions_menu.length) return;

        let observer = new MutationObserver(function() {
            frm.remove_custom_button('Reverse Journal Entry', 'Actions');
        });

        observer.observe($actions_menu[0], { childList: true, subtree: true });

        // Turant bhi ek baar try karo (agar already add ho chuka ho)
        frm.remove_custom_button('Reverse Journal Entry', 'Actions');

        // Form navigate away hone pr observer band kar do (memory leak avoid)
        frm.page.wrapper.on('hide', () => observer.disconnect());
    }
});