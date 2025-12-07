from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_health_check():

    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {
        "status": "healthy"
    }


def test_risk_check_returns_decision():

    request = {
        "merchant_id": "merchant-1",
        "checkout_id": "checkout-1",
        "customer": {
            "id": "customer-1",
            "email": "customer@example.com",
        },
        "payment": {
            "amount": 1500,
            "currency": "GBP",
            "bin_country": "US",
        },
        "device": {
            "id": "device-1",
            "ip_address": "127.0.0.1",
        },
        "shipping": {
            "country": "GB",
        },
    }

    response = client.post(
        "/v1/risk/check",
        json=request,
    )

    assert response.status_code == 200

    body = response.json()

    assert "request_id" in body
    assert "risk_score" in body
    assert "risk_level" in body
    assert "decision" in body
    assert "reasons" in body