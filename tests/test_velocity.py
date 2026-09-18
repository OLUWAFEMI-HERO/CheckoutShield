import pytest

from app.services.velocity import (
    VelocityService,
)


@pytest.mark.asyncio
async def test_velocity_allows_requests_until_limit():

    service = VelocityService(
        time_window_seconds=60,
        max_attempts=2,
    )

    assert await service.check_and_record(
        "merchant:customer"
    ) is True

    assert await service.check_and_record(
        "merchant:customer"
    ) is True

    assert await service.check_and_record(
        "merchant:customer"
    ) is False


@pytest.mark.asyncio
async def test_velocity_isolated_by_identifier():

    service = VelocityService(
        max_attempts=1
    )

    assert await service.check_and_record(
        "merchant:a"
    ) is True

    assert await service.check_and_record(
        "merchant:b"
    ) is True


@pytest.mark.asyncio
async def test_velocity_can_be_reset():

    service = VelocityService(
        max_attempts=1
    )

    await service.check_and_record(
        "merchant:customer"
    )

    await service.reset()

    assert await service.check_and_record(
        "merchant:customer"
    ) is True

class VelocityService:

    def __init__(
        self,
        time_window_seconds: int = 60,
        max_attempts: int = 5,
        clock=time.monotonic,
    ) -> None:

        self.time_window = time_window_seconds
        self.max_attempts = max_attempts
        self._clock = clock


@pytest.mark.asyncio
async def test_concurrent_requests_respect_velocity_limit():

    service = VelocityService(
        max_attempts=1
    )

    results = await asyncio.gather(
        service.check_and_record("merchant:customer"),
        service.check_and_record("merchant:customer"),
    )

    assert results.count(True) == 1
    assert results.count(False) == 1