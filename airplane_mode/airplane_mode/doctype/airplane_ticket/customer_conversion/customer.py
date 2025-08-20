import frappe

def get_or_create_customer(passenger):
    customer = frappe.db.exists("Customer", {"customer_name": passenger.full_name})
    if customer:
        return customer

    new_customer = frappe.get_doc({
        "doctype": "Customer",
        "customer_name": passenger.full_name,
        "customer_type": "Individual"
    })
    new_customer.insert()
    return new_customer.name
