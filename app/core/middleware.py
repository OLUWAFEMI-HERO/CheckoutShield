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