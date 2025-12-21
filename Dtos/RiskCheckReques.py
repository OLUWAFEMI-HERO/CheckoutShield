class RiskCheckRequest(CheckoutValidationMixin):
    merchant_id: str
    checkout_id: str
    customer: Customer
    payment: Payment
    device: Device
    shipping: Shipping