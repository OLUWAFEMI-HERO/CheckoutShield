def test_missing_request_returns_none():

    repository = InMemoryAssessmentRepository()

    assert repository.get(
        "missing"
    ) is None


def test_recent_limit_returns_requested_number():

    repository = InMemoryAssessmentRepository()

    for index in range(5):
        repository.save(
            "merchant",
            f"checkout-{index}",
            result(f"request-{index}"),
        )

    recent = repository.list_recent(
        limit=2
    )

    assert [
        item.request_id
        for item in recent
    ] == [
        "request-4",
        "request-3",
    ]
def test_repository_retains_most_recent_records():

    repository = InMemoryAssessmentRepository()

    for index in range(3):
        repository.save(
            "merchant",
            f"checkout-{index}",
            result(f"request-{index}"),
        )

    recent = repository.list_recent(
        limit=2
    )

    assert [
        item.request_id
        for item in recent
    ] == [
        "request-2",
        "request-1",
    ]