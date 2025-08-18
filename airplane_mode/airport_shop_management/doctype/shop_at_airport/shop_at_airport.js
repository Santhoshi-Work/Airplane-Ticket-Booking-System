// Copyright (c) 2025, Navtech and contributors
// For license information, please see license.txt

// Copyright (c) 2025, Navtech and contributors
// For license information, please see license.txt

frappe.ui.form.on('Shop At Airport', {
    setup: function(frm) {
        // Filter shop_type to only enabled types
        frm.set_query('shop_type', function() {
            return {
                filters: {
                    enabled: 1
                }
            };
        });
    
    },

    onload: function(frm) {
        // Fetch default rent from Global Configuration
        frappe.db.get_single_value('Shop Settings', 'default_rent_amount')
            .then(default_rent_amount => {
                if (!frm.doc.monthly_rent) {
                    frm.set_value('monthly_rent', default_rent_amount);
                }
            });

        // You can add more default fields from Global Configuration here
        // e.g., rent_reminder_days, default_lease_term, etc.
    }
});

