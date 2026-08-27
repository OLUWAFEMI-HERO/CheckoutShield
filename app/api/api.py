# checkout_shield/api.py
from fastapi import FastAPI, HTTPException, status
from checkout_shield.schemas import CheckoutRequest, ShieldResponse
from checkout_shield.agent import AgenticFraudEvaluator
from checkout_shield.notifier import AlertNotifier

app = FastAPI(
    title="CheckoutShield API",
    description="Real-time Agentic Transaction Security & Fraud Detection Engine",
    version="1.0.0"
)

evaluator = AgenticFraudEvaluator(max_allowed_amount=3000.0)
notifier = AlertNotifier(webhook_url="https://api.checkoutshield.internal/hooks/alerts")

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