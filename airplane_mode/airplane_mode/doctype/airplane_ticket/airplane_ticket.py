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
		self.set_seat()
		
	# set seat function is for patch !!
	def set_seat(self):
		self.seat = f"{random.randint(1, 100)}{random.choice(string.ascii_uppercase[:5])}"

		# self.seat=f"{random.randint(1,100)}{random.choice(['A','B','C','D','E'])}"
	# self.seat = f"{random.randint(1, 100)}{random.choice(string.ascii_uppercase[:5])}"
	# def before_save(self):
	# 	self.cost = sum([item.amount or 0 for item in self.add_ons])
	# 	self.total_amount = (self.flight_price or 0) + (self.cost or 0)
	def before_insert(self):
		self.seat = f"{random.randint(1, 100)}{random.choice(string.ascii_uppercase[:5])}"
	def before_submit(self):
		if self.status!="Boarded":
			frappe.throw(" STATUS SHOULD BE BOARDED")
		create_payment_schedule(self)
			
	# def on_submit(self):
	# 	if not self.ticket_payment_schedule:
	# 			create_payment_schedule(self)

	def check_seat_availability(self):
		if not self.flight:
			return

        # Get the flight document
		flight = frappe.get_doc("Airplane Flight", self.flight)

        # Get airplane and its capacity
		if not flight.airplane:
			frappe.throw(_("This flight has no airplane assigned."))
		
		airplane = frappe.get_doc("Airplane", flight.airplane)
		capacity = airplane.capacity

        # Count confirmed tickets for this flight (excluding current draft)
		ticket_count = frappe.db.count(
		"Airplane Ticket",
            {
                "flight": self.flight,
                "docstatus": ["<", 2],
                "name": ["!=", self.name]  # exclude current unsaved doc
            }
        )
		if ticket_count >= capacity:
			frappe.throw("No more seats available for this flight")

	






