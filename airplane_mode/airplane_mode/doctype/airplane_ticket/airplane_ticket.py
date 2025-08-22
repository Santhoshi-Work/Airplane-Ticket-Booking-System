# Copyright (c) 2025, Navtech and contributors
# For license information, please see license.txt

# Copyright (c) 2025, Navtech and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
import random
import string
from frappe import _, throw
from .installments.gen_installments import create_payment_schedule
from .customer_conversion.customer import get_or_create_customer


class AirplaneTicket(Document):
	def validate(self):
		unique_add_ons = []
		seen = set()

		for item in self.add_ons:
			if item.item not in seen:
				seen.add(item.item)
				unique_add_ons.append(item)

		self.add_ons = unique_add_ons
		self.cost = sum([item.amount or 0 for item in self.add_ons])
		self.total_amount = (self.flight_price or 0) + (self.cost or 0)
		self.check_seat_availability()
		create_payment_schedule(self)
		print(self.ticket_payment_schedule)
		#self.set_seat()
		
	# set seat function is for patch !!
	def set_seat(self):
		self.seat = f"{random.randint(1, 100)}{random.choice(string.ascii_uppercase[:5])}"



	def before_insert(self):
		self.seat = f"{random.randint(1, 100)}{random.choice(string.ascii_uppercase[:5])}"


	def before_submit(self):
		if self.status!="Boarded":
			frappe.throw(" STATUS SHOULD BE BOARDED")
		create_payment_schedule(self)

	def on_submit(self):
		passenger = frappe.get_doc("Flight Passenger", self.passenger)
		customer_name = get_or_create_customer(passenger)
		invoice = frappe.new_doc("Sales Invoice")
		invoice.customer = customer_name
		invoice.custom_airplane_ticket = self.name
		invoice.posting_date = frappe.utils.nowdate()
		invoice.due_date = frappe.utils.add_days(invoice.posting_date, 7)
		default_income_account = frappe.get_value(
        "Company", self.company, "default_income_account"
    ) or "Sales - NAV"
		default_cost_center = frappe.get_value(
        "Company", self.company, "cost_center"
    ) or "Main - NAV"
		
		invoice.append("items", {
            "item_name": f"Flight {self.flight} ({self.source_airport_code} → {self.destination_airport_code})",
            "qty": 1,
            "rate": round(self.total_amount,2),
            "amount": round(self.total_amount,2),
			"income_account": default_income_account,
			"cost_center":default_cost_center
        })

		invoice.insert()
		invoice.submit()

		frappe.msgprint(f"ERPNext Invoice {invoice.name} created for ticket {self.name}")

		self.create_payment_entry_for_ticket(invoice)

	def create_payment_entry_for_ticket(self, invoice):
		payment_entry = frappe.get_doc({
        "doctype": "Payment Entry",
        "payment_type": "Receive",
        "party_type": "Customer",
        "party": invoice.customer,
        "posting_date": frappe.utils.nowdate(),
        "mode_of_payment": "Cash", 
		"paid_to":"Cash - NAV",
		"paid_to_account_currency": "INR",
        "paid_amount": invoice.grand_total,
        "received_amount": invoice.grand_total,
		 "target_exchange_rate": 1.0,
        "references": [
            {
                "reference_doctype": "Sales Invoice",
                "reference_name": invoice.name,
                "allocated_amount": invoice.grand_total
            }
        ]
    })
		payment_entry.insert(ignore_permissions=True)  
		frappe.msgprint(f"Draft Payment Entry {payment_entry.name} created for Invoice {invoice.name}")

	# def on_update(self):
	# 	if self.status == "Paid":
	# 		invoice_name = frappe.db.get_value(
    #         "Sales Invoice", {"custom_airplane_ticket": self.name}
    #     	)
	# 		if invoice_name:
	# 			exists = frappe.db.exists(
    #             "Payment Entry",
    #             {"reference_name": invoice_name, "docstatus": 1}
    #         )
	# 			if not exists:
	# 				invoice = frappe.get_doc("Sales Invoice", invoice_name)
	# 				paid_amount = invoice.grand_total
	# 				pe = frappe.get_doc({
    #                 "doctype": "Payment Entry",
    #                 "payment_type": "Receive",
    #                 "party_type": "Customer",
    #                 "party": invoice.customer,
    #                 "posting_date": frappe.utils.nowdate(),
    #                 "mode_of_payment": "Cash",   # 👈 or Bank Draft if you prefer
    #                 "paid_from": frappe.get_value("Company", self.company, "default_cash_account"),
    #                 "paid_to": frappe.get_value("Company", self.company, "default_receivable_account"),
    #                 "paid_amount": paid_amount,
    #                 "received_amount": paid_amount,
    #                 "reference_no": self.name,
    #                 "reference_date": frappe.utils.nowdate(),
    #                 "references": [{
    #                     "reference_doctype": "Sales Invoice",
    #                     "reference_name": invoice_name,
    #                     "total_amount": paid_amount,
    #                     "allocated_amount": paid_amount,
    #                 }]
    #             })
	# 			pe.insert(ignore_permissions=True)
	# 			pe.submit()
	# 			frappe.db.commit()
	# 			frappe.msgprint(f"Invoice {invoice_name} marked as Paid via Payment Entry {pe.name}")



	def check_seat_availability(self):
		if not self.flight:
			return

		flight = frappe.get_doc("Airplane Flight", self.flight)

 
		if not flight.airplane:
			frappe.throw(_("This flight has no airplane assigned."))
		
		airplane = frappe.get_doc("Airplane", flight.airplane)
		capacity = airplane.capacity

   
		ticket_count = frappe.db.count(
		"Airplane Ticket",
            {
                "flight": self.flight,
                "docstatus": ["<", 2],
                "name": ["!=", self.name] 
            }
        )
		if ticket_count >= capacity:
			frappe.throw("No more seats available for this flight")

	






