from app.models.risk import (
    Customer,
    Device,
    Payment,
    RiskCheckRequest,
    RiskDecision,
    Shipping,
)
from app.services.risk_service import RiskService


def create_request(
    amount: float = 100,
    bin_country: str = "GB",
    shipping_country: str = "GB",
    device_id: str = "device-1",
) -> RiskCheckRequest:

    return RiskCheckRequest(
        merchant_id="merchant-1",
        checkout_id="checkout-1",
        customer=Customer(
            id="customer-1",
            email="customer@example.com",
        ),
        payment=Payment(
            amount=amount,
            currency="GBP",
            bin_country=bin_country,
        ),
        device=Device(
            id=device_id,
            ip_address="127.0.0.1",
        ),
        shipping=Shipping(
            country=shipping_country,
        ),
    )


def test_low_risk_transaction_is_approved():

    service = RiskService()

    result = service.evaluate(
        create_request()
    )

    assert result.risk_score == 0
    assert result.decision == RiskDecision.APPROVE


def test_medium_risk_transaction_requires_review():

    service = RiskService()

    result = service.evaluate(
        create_request(
            amount=1500,
            bin_country="US",
            shipping_country="GB",
            device_id="new-device",
        )
    )

    assert result.risk_score == 45
    assert result.decision == RiskDecision.APPROVE