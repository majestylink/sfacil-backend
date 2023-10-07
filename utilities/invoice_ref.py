def generate_invoice_ref():
    import time
    import random
    timestamp = int(time.time())  # Current timestamp
    random_number = random.randint(1000, 9999)  # Random 4-digit number
    return f"INV-{timestamp}-{random_number}"
