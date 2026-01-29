from pydantic import BaseModel, EmailStr, condecimal

class CheckoutPayload(BaseModel):
    user_email: EmailStr
    amount: condecimal(gt=0, max_digits=10, decimal_places=2) # Must be greater than 0
    currency: str
    ip_address: str

# Testing the validation
try:
    # If the data is bad, this throws a validation error immediately
    data = CheckoutPayload(
        user_email="customer@example.com", 
        amount=150.00, 
        currency="USD", 
        ip_address="192.168.1.1"
    )
    print("Payload is clean and shielded!")
except Exception as e:
    print(f"Validation failed: {e}")