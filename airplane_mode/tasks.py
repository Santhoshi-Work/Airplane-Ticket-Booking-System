import frappe 
def update_ticket_gates(doc, method):
    tickets = frappe.get_all(
        "Airplane Ticket",
        filters={"flight": doc.name},  # use name, not the doc object
        fields=["name"]
    )

    for ticket in tickets:
        frappe.db.set_value("Airplane Ticket", ticket.name, "gate_number", doc.gate_number)
