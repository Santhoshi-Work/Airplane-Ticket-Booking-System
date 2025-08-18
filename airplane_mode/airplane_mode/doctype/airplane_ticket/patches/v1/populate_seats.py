import frappe

def execute():
    tickets = frappe.get_all("Airplane Ticket", fields=["name", "seat", "flight"])

    for ticket in tickets:
        if not ticket["seat"]:
            # Check if the linked flight exists before saving
            if not frappe.db.exists("Airplane Flight", ticket["flight"]):
                frappe.log_error(f"Skipping {ticket['name']} - Flight {ticket['flight']} does not exist.")
                continue

            d = frappe.get_doc("Airplane Ticket", ticket["name"])
            d.set_seat()
            d.save()

    frappe.db.commit()