def test_expired_idempotency_result_is_removed():

    current_time = 100.0

    def clock():
        return current_time

    service = IdempotencyService(
        ttl_seconds=60,
        clock=clock,
    )

    payload = {
        "amount": 100,
    }

    service.store(
        "key-expiring",
        payload,
        {"request_id": "abc"},
    )

    assert service.get(
        "key-expiring",
        payload,
    ) == {
        "request_id": "abc"
    }

    current_time = 161.0

    assert service.get(
        "key-expiring",
        payload,
    ) is None