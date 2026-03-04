# tests/test_shield.py
import pytest
from checkout_shield.schemas import CheckoutRequest, ItemDetail, RiskLevel
from checkout_shield.agent import AgenticFraudEvaluator

@pytest.fixture
def evaluator():
    return AgenticFraudEvaluator(max_allowed_amount=2000.0, high_risk_countries=["XX"])

@pytest.fixture
def clean_payload():
    return CheckoutRequest(
        transaction_id="tx_10001",
        user_email="buyer@validcompany.com",
        amount=150.00,
        currency="USD",
        ip_address="192.168.1.1",
        billing_country="US",
        shipping_country="US",
        items=[ItemDetail(item_id="it_1", name="Wireless Mouse", quantity=1, price=150.00)]
    )

def test_clean_transaction_approval(evaluator, clean_payload):
    result = evaluator.evaluate(clean_payload)
    assert result.is_approved is True
    assert result.risk_level == RiskLevel.LOW
    assert result.risk_score == 0

def test_high_risk_flagging(evaluator, clean_payload):
    clean_payload.amount = 5000.00  # Exceeds max allowed
    clean_payload.shipping_country = "XX"  # Blocklisted country
    clean_payload.user_email = "scammer@tempmail.com"  # Disposable domain

    result = evaluator.evaluate(clean_payload)
    assert result.is_approved is False
    assert result.risk_level == RiskLevel.CRITICAL
    assert result.risk_score >= 70
    assert len(result.reasons) == 3