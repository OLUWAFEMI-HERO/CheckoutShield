def test_negative_amount_is_rejected():

    payload = valid_request()
    payload["payment"]["amount"] = -10

    response = client.post(
        "/v1/risk/check",
        json=payload,
    )

    assert response.status_code == 422


def test_missing_customer_is_rejected():

    payload = valid_request()
    payload.pop("customer")

    response = client.post(
        "/v1/risk/check",
        json=payload,
    )

    assert response.status_code == 422


def test_invalid_currency_length_is_rejected():

    payload = valid_request()
    payload["payment"]["currency"] = "GB"

    response = client.post(
        "/v1/risk/check",
        json=payload,
    )

    assert response.status_code == 422