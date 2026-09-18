def test_generated_correlation_id_is_valid_uuid():

    import uuid

    client = TestClient(create_app())

    response = client.get("/health")

    correlation_id = (
        response.headers["X-Correlation-ID"]
    )

    uuid.UUID(correlation_id)


def test_process_time_is_non_negative():

    client = TestClient(create_app())

    response = client.get("/health")

    processing_time = float(
        response.headers["X-Process-Time-Ms"]
    )

    assert processing_time >= 0

class ProcessTimeMiddleware(BaseHTTPMiddleware):

    async def dispatch(
        self,
        request: Request,
        call_next,
    ):
        start = time.perf_counter()

        response = await call_next(request)

        elapsed_ms = (
            time.perf_counter() - start
        ) * 1000

        response.headers[
            PROCESS_TIME_HEADER
        ] = f"{elapsed_ms:.2f}"

        return response