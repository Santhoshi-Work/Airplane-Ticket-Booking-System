# Copyright (c) 2025, Navtech and contributors
import frappe
from frappe.website.website_generator import WebsiteGenerator

class AirplaneFlight(WebsiteGenerator):
    def on_submit(self):
        # safer than self.save()
        self.db_set("status", "Completed")
        
        tickets = frappe.get_all(
            "Airplane Ticket",
            filters={"flight": self.name, "status": "Boarded", "docstatus": 0},
            fields=["name"],
        )
        frappe.msgprint(f"Found {len(tickets)} ticket(s) to submit.")

        for ticket in tickets:
            try:
                frappe.get_doc("Airplane Ticket", ticket.name).submit()
            except Exception as e:
                frappe.msgprint(f"Could not submit ticket {ticket.name}: {e}")

    def on_update_after_submit(self):
        """Only fire when doc is already submitted and updated"""
        self.enqueue_gate_update()

    def enqueue_gate_update(self):
        frappe.enqueue(
            "airplane_mode.tasks.update_ticket_gates",
            queue="default",
            timeout=300,
            job_name=f"Update ticket gates for {self.name}",
            flight_name=self.name,
            new_gate=self.gate_number,
        )
