import frappe
from frappe.utils import add_days, nowdate

def generate_installments(self):
    """Return list of installments (due_date + amount)"""
    settings = frappe.get_single("Flight Settings")

    # Full payment → single installment
    if self.payment_plan == "Full":
        return [{
            "due_date": nowdate(),
            "amount": self.total_amount
        }]

    # Installments → equal split
    installments = []
    count = settings.installment_count or 3
    interval = settings.installment_interval_days or 30

    per_installment = self.total_amount / count

    for i in range(count):
        due_date = add_days(nowdate(), i * interval)
        installments.append({
            "due_date": due_date,
            "amount": per_installment
        })

    return installments


def create_payment_schedule(self):
    """Attach generated installments to the ticket's child table"""
    self.ticket_payment_schedule = [] 
    installments = generate_installments(self)

    for inst in installments:
        self.append("ticket_payment_schedule", {
            "due_date": inst["due_date"],
            "amount": inst["amount"],
            "status": "Unpaid"
        })
