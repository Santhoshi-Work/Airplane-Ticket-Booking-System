// Copyright (c) 2025, Navtech and contributors
// For license information, please see license.txt

// Copyright (c) 2025, Navtech and contributors
// For license information, please see license.txt

frappe.ui.form.on('Shop At Airport', {
  setup: function(frm) {
    frm.set_query('shop_type', function() {
      return {
        filters: {
          enabled: 1
        }
      };
    });
  }
});

