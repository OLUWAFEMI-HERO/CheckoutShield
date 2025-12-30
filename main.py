from fastapi import FastAPI

from app.api.risk import router as risk_router

app = FastAPI(
    title="CheckoutShield",
    description="Real-time checkout risk and fraud decisioning for e-commerce.",
    version="0.1.0",
)

app.include_router(risk_router)