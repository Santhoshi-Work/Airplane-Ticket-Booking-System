# Copyright (c) 2025, Navtech and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class ShopLeaseContract(Document):
    def validate(self):
        self.set_total_rent()
        # self.validate_dates()
        self.validate_duplicate_shops()

    def set_total_rent(self):
        self.total_rent = sum(item.monthly_rent for item in self.shops_leased)

    # def validate_dates(self):
    #     if self.lease_end_date <= self.lease_start_date:
    #         frappe.throw("Lease End Date must be after Start Date.")
    #     else:
    #         frappe.throw("Please enter both Lease Start Date and Lease End Date.")
    

    def validate_duplicate_shops(self):
        seen = set()
        for item in self.shops_leased:
            if item.shop in seen:
                frappe.throw(f"Duplicate shop found: {item.shop}")
            seen.add(item.shop)

    def on_submit(self):
        if self.status == "Terminated":
            for item in self.shops_leased:
            # Get the linked Shop document
                shop_doc = frappe.get_doc("Shop At Airport", item.shop)
                shop_doc.shop_status = "Available"  # or whatever field tracks availability
                shop_doc.save(ignore_permissions=True)

        current_status = frappe.db.get_value("Shop Lease Contract", self.name, "status") or "Draft"
        tenant_exists = frappe.db.exists("Tenant Information", {"email_id": self.email_id})
        if not tenant_exists:
            tenant = frappe.new_doc("Tenant Information")
            tenant.full_name = self.full_name
            tenant.email_id = self.email_id
            tenant.phone = self.phone
            tenant.insert(ignore_permissions=True)
            frappe.msgprint(f"Tenant Information '{self.full_name}' created.")

        for row in self.shops_leased:
            if row.shop:
                current_status = frappe.db.get_value("Shop At Airport", row.shop, "status")
            if current_status != "Leased":
                frappe.db.set_value("Shop At Airport", row.shop, "status", "Leased")  

    def on_cancel(self):
        for item in self.shops_leased:
            if item.shop and frappe.db.exists("Shop At Airport", item.shop):
                current_status = frappe.db.get_value("Shop At Airport", item.shop, "status")
            if current_status != "Available":
                frappe.db.set_value("Shop At Airport", item.shop, "status", "Available")
                frappe.msgprint(f"{item.shop} status set to Available.")
