// Copyright (c) 2025, Navtech and contributors
// For license information, please see license.txt


frappe.ui.form.on('Airline', {
    refresh: function (frm) {
        // Showing web link only if the website field is filled
        if (frm.doc.website) {
            frm.add_web_link(frm.doc.website, 'Visit Website');
        }
    }
});
