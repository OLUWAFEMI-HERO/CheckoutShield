# checkout_shield/middleware.py
import uuid
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

class CorrelationIdMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        correlation_id = request.headers.get("X-Correlation-ID", str(uuid.uuid4()))
        
        # Attach to request state so routes can access it
        request.state.correlation_id = correlation_id
        
        response = await call_next(request)
        
        # Return it to the client
        response.headers["X-Correlation-ID"] = correlation_id
        return response