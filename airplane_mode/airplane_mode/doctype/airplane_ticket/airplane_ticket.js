// Copyright (c) 2025, Navtech and contributors
// For license information, please see license.txt

frappe.ui.form.on("Airplane Ticket", {
    refresh: function(frm) {
        frm.add_custom_button("Assign Seat", () => {
            frappe.prompt(
                [
                    {
                        fieldname: "seat",
                        label: "Seat Number",
                        fieldtype: "Data",
                        reqd: 1
                    }
                ],
                (values) => {
                    frm.set_value("seat", values.seat);
                },
                __("Assign Seat"),
                __("Assign")
            );
        }, __("Actions"));  
    }
});
