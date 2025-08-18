# Copyright (c) 2025, Navtech and contributors
# For license information, please see license.txt

import frappe
from frappe.website.website_generator import WebsiteGenerator



# def before_save(doc, method):
#     if not doc.monthly_rent:
#         default_rent = frappe.db.get_single_value('Shop Settings', 'default_rent')
#         doc.monthly_rent = default_rent
def default_rent(doc, method):
    settings = frappe.get_single("Shop Settings")
    if not doc.get("monthly_rent") and settings.get("default_rent_amount"):
        doc.monthly_rent = settings.default_rent_amount


class ShopAtAirport(WebsiteGenerator):
	pass
