import frappe

def get_context(context):
    shop_name = frappe.form_dict.get("shop")
    if not shop_name:
        frappe.throw("Shop parameter missing")

    try:
        context.shop = frappe.get_doc("Shop At Airport", shop_name)
    except frappe.DoesNotExistError:
        frappe.throw("Shop not found")

    return context