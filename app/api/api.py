# checkout_shield/api.py
from fastapi import FastAPI, HTTPException, status
from checkout_shield.schemas import CheckoutRequest, ShieldResponse
from checkout_shield.agent import AgenticFraudEvaluator
from checkout_shield.notifier import AlertNotifier
from fastapi import FastAPI, HTTPException, status, Depends, BackgroundTasks, Request
from sqlalchemy.orm import Session
from checkout_shield.schemas import CheckoutRequest, ShieldResponse
from checkout_shield.agent import AgenticFraudEvaluator
from checkout_shield.notifier import AlertNotifier
from checkout_shield.config import settings
from checkout_shield.auth import verify_api_key
from checkout_shield.database import get_db, AssessmentRecord
from checkout_shield.velocity import velocity_engine
from checkout_shield.middleware import CorrelationIdMiddleware

app.add_middleware(CorrelationIdMiddleware)

app = FastAPI(
    title="CheckoutShield API",
    description="Real-time Agentic Transaction Security & Fraud Detection Engine",
    version="1.0.0"
)

evaluator = AgenticFraudEvaluator()
notifier = AlertNotifier(webhook_url=settings.webhook_url)

@app.post("/api/v1/shield/evaluate", response_model=ShieldResponse)

@app.post(
    "/api/v1/shield/evaluate",
    response_model=ShieldResponse,
    status_code=status.HTTP_200_OK
)
async def evaluate_checkout(payload: CheckoutRequest):
    try:
        assessment = evaluator.evaluate(payload)
        await notifier.notify_if_flagged(assessment)
        return assessment
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error evaluating checkout payload: {str(e)}"
        )

@app.get("/health")
def health_check():
    return {"status": "active", "engine": "CheckoutShield Agentic v1.0"}


async def evaluate_checkout(
    request: Request,
    payload: CheckoutRequest,
    background_tasks: BackgroundTasks,
    api_key: str = Depends(verify_api_key),
    db: Session = Depends(get_db)
):
    # 1. Check Velocity (Rate limiting logic)
    if not velocity_engine.check_and_record(payload.user_email):
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Velocity limit exceeded for this email."
        )

    # 2. Evaluate via Agent
    assessment = evaluator.evaluate(payload)

    # 3. Save to Database asynchronously (Non-blocking)
    def save_to_db(record: ShieldResponse):
        db_record = AssessmentRecord(
            transaction_id=record.transaction_id,
            user_email=payload.user_email,
            amount=payload.amount,
            is_approved=record.is_approved,
            risk_level=record.risk_level.value,
            risk_score=record.risk_score
        )
        db.add(db_record)
        db.commit()
        
    background_tasks.add_task(save_to_db, assessment)

    # 4. Trigger webhooks asynchronously
    background_tasks.add_task(notifier.notify_if_flagged, assessment)

    return assessment