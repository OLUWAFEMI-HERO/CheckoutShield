from app.models.risk import (
    Customer,
    Device,
    Payment,
    RiskCheckRequest,
    Shipping,
)
from app.services.rules import (
    check_country_mismatch,
    check_high_value_transaction,
    check_new_device,
)


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


def test_high_value_transaction_is_flagged():
    request = create_request(amount=1500)

    result = check_high_value_transaction(request)

    assert result is not None
    assert result[0] == 20


def test_normal_transaction_is_not_flagged():
    request = create_request(amount=100)

    result = check_high_value_transaction(request)

    assert result is None


def test_country_mismatch_is_flagged():
    request = create_request(
        bin_country="US",
        shipping_country="GB",
    )

    result = check_country_mismatch(request)

    assert result is not None
    assert result[0] == 15


def test_matching_country_is_not_flagged():
    request = create_request(
        bin_country="GB",
        shipping_country="GB",
    )

    result = check_country_mismatch(request)

    assert result is None


def test_new_device_is_flagged():
    request = create_request(
        device_id="new-device-1",
    )

    result = check_new_device(request)

    assert result is not None
    assert result[0] == 10