# tools/payment_gateway.py
def process_payment(amount):
    # Simulate payment processing (integrate with a real payment API as needed)
    try:
        amount = float(amount)
    except:
        amount = 0
    if amount > 0:
        return {"status": "success", "transaction_id": "TX123456"}
    else:
        return {"status": "failed"}