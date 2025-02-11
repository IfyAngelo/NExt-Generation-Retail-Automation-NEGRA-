# tools/email_service.py
def send_invoice_email(email_address, cart_items, cart_total):
    # Simulate sending an invoice email (integrate with an email API as needed)
    if email_address:
        return {"status": "sent", "email": email_address}
    else:
        return {"status": "failed"}