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


def test_idempotent_retry_returns_same_request_id():

    payload = _valid_payload()

    headers = {
        "Idempotency-Key": "performance-idempotency"
    }

    first = client.post(
        "/v1/risk/check",
        json=payload,
        headers=headers,
    )

    second = client.post(
        "/v1/risk/check",
        json=payload,
        headers=headers,
    )

    assert first.status_code == 200
    assert second.status_code == 200

    assert (
        second.json()["request_id"]
        == first.json()["request_id"]
    )


def test_idempotency_conflict_returns_409():

    payload = _valid_payload()

    headers = {
        "Idempotency-Key": "conflict-test"
    }

    first = client.post(
        "/v1/risk/check",
        json=payload,
        headers=headers,
    )

    changed_payload = _valid_payload()
    changed_payload["payment"]["amount"] = 500

    second = client.post(
        "/v1/risk/check",
        json=changed_payload,
        headers=headers,
    )

    assert first.status_code == 200
    assert second.status_code == 409

def test_risk_check_persists_and_returns_decision():

    payload = _valid_payload()

    response = client.post(
        "/v1/risk/check",
        json=payload,
    )

    assert response.status_code == 200

    body = response.json()

    assert body["risk_score"] == 0
    assert body["risk_level"] == "LOW"
    assert body["decision"] == "APPROVE"
    assert body["reasons"] == []

    request_id = body["request_id"]

    retrieved = client.get(
        f"/v1/risk/decisions/{request_id}"
    )

    assert retrieved.status_code == 200
    assert retrieved.json() == body