import frappe
from frappe.model.document import Document

class RentPayment(Document):

    def on_submit(self):
        """Generate receipt and send email if enabled in Shop Settings"""
        self.generate_and_attach_receipt()
        self.send_rent_receipt_email_if_enabled()

    def generate_and_attach_receipt(self):
        """Generate PDF from Print Format and attach to the document"""
        pdf = frappe.get_print(
            doctype="Rent Payment",
            name=self.name,
            print_format="Rent Receipt",
            as_pdf=True
        )

        # Attach PDF to Rent Payment
        file_doc = frappe.get_doc({
            "doctype": "File",
            "file_name": f"RentReceipt-{self.name}.pdf",
            "attached_to_doctype": self.doctype,
            "attached_to_name": self.name,
            "content": pdf,
            "is_private": 1
        })
        file_doc.save()

        # Save file URL in a field (optional)
        self.receipt = file_doc.file_url
        self.save(ignore_permissions=True)
        self.add_comment("Attachment", "Rent receipt auto-generated and attached.")

    def send_rent_receipt_email_if_enabled(self):
        """Send rent receipt email only if Shop Settings enable it"""
        # Get Shop Settings
        shop_settings = frappe.get_single("Shop Settings")
        if not shop_settings.enable_rent_reminders:
            return

        # Get tenant email from linked Lease Contract
        if not self.lease_contract:
            frappe.log_error(f"Lease Contract not linked for Rent Payment {self.name}", "Rent Payment Email Skipped")
            return

        lease_contract = frappe.get_doc("Shop Lease Contract", self.lease_contract)
        tenant_email = getattr(lease_contract, "email_id", None)
        if not tenant_email:
            frappe.log_error(f"No email found for tenant in Lease Contract {lease_contract.name}", "Rent Payment Email Skipped")
            return

        # Generate PDF again for email attachment
        pdf = frappe.get_print(
            doctype="Rent Payment",
            name=self.name,
            print_format="Rent Receipt",
            as_pdf=True
        )

        # Send email
        frappe.sendmail(
            recipients=[tenant_email],
            subject=f"Rent Receipt - {self.name}",
            message="Thank you for your payment. Please find your rent receipt attached.",
            attachments=[{
                "fname": f"RentReceipt-{self.name}.pdf",
                "fcontent": pdf,
                "content_type": "application/pdf"
            }],
            reference_doctype=self.doctype,
            reference_name=self.name
        )
        frappe.msgprint(f"Rent receipt emailed to {tenant_email}.")
