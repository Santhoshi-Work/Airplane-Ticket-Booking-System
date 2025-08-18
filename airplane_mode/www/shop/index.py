import frappe

def get_context(context):
    context.shops = frappe.get_all(
        "Shop At Airport",
        filters={"is_published": 1},
        fields=["name", "shop_name", "airport", "status"]
    )
    return context
