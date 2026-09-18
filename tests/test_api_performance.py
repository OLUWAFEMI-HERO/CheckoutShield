def test_risk_check_stays_within_latency_budget():

    response = client.post(
        "/v1/risk/check",
        json=valid_payload(),
    )

    assert response.status_code == 200

    elapsed_ms = float(
        response.headers["X-Process-Time-Ms"]
    )

    assert elapsed_ms < 100
def test_repeated_risk_checks_remain_within_latency_budget():

    timings = []

    for index in range(20):

        payload = valid_payload()

        payload["checkout_id"] = (
            f"checkout-performance-{index}"
        )

        response = client.post(
            "/v1/risk/check",
            json=payload,
        )

        assert response.status_code == 200

        timings.append(
            float(
                response.headers[
                    "X-Process-Time-Ms"
                ]
            )
        )

    average_latency = (
        sum(timings) / len(timings)
    )

    assert average_latency < 100