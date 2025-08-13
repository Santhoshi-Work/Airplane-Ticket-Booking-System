# Copyright (c) 2025, Navtech and contributors
# For license information, please see license.txt

# Copyright (c) 2025, NAV and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import getdate

class ShopLeaseRequest(Document):
    
    def on_submit(self):
        # Set status to Approved on submit
        self.status = "Approved"
        self.db_set("status", "Approved")

        # Automatically create lease contract upon approval
        self.create_lease_contract_if_not_created()

    def create_lease_contract_if_not_created(self):
        # Prevent duplicate contracts
        existing_contract = frappe.db.exists("Shop Lease Contract", {
            "full_name": self.full_name,
            "lease_start_date": self.lease_start_date
        })
        if existing_contract:
            frappe.msgprint("Lease Contract already exists.")
            return

        # Generate a new name for the contract
        full_name = self.full_name.replace(" ", "-").lower()
        date_str = getdate(self.lease_start_date).strftime("%Y%m%d")
        base_name = f"LEASE-{full_name}-{date_str}"
        contract_name = base_name
        counter = 1

        while frappe.db.exists("Shop Lease Contract", contract_name):
            contract_name = f"{base_name}-{counter}"
            counter += 1

        # Create the contract
        lease_contract = frappe.new_doc("Shop Lease Contract")
        lease_contract.name = self.name
        lease_contract.full_name = self.full_name
        lease_contract.phone = self.phone
        lease_contract.email_id = self.email_id
        lease_contract.lease_start_date = self.lease_start_date
        lease_contract.lease_end_date = self.lease_end_date
        lease_contract.status = "Draft"

        total_rent = 0

        for item in self.shops_leased:
            if not frappe.db.exists("Shop At Airport", item.shop):
                frappe.throw(f"🚫 Shop '{item.shop_name}' not found in Shop At Airport.")

            shop_doc = frappe.get_doc("Shop At Airport", item.shop)

            lease_contract.append("shops_leased", {
                "shop": shop_doc.name,
                "monthly_rent": shop_doc.monthly_rent
            })
            total_rent += shop_doc.monthly_rent

        lease_contract.total_rent = total_rent

        try:
            lease_contract.insert(ignore_permissions=True)
            frappe.msgprint(f"✅ Lease Contract {lease_contract.name} created successfully.")
        except Exception as e:
            frappe.throw(f"Error creating contract: {e}")