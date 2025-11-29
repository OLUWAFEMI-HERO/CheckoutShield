from fastapi import APIRouter

from app.models.risk import (
    RiskCheckRequest,
    RiskCheckResponse,
)
from app.services.risk_service import RiskService


router = APIRouter(
    prefix="/v1/risk",
    tags=["Risk"],
)

risk_service = RiskService()


@router.post(
    "/check",
    response_model=RiskCheckResponse,
)
async def check_risk(
    request: RiskCheckRequest,
) -> RiskCheckResponse:

    return risk_service.evaluate(request)