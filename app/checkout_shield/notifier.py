# checkout_shield/notifier.py
import logging
from checkout_shield.schemas import ShieldResponse, RiskLevel

logger = logging.getLogger("CheckoutShieldNotifier")
logging.basicConfig(level=logging.INFO)

class AlertNotifier:
    def __init__(self, webhook_url: str = None):
        self.webhook_url = webhook_url

    async def notify_if_flagged(self, assessment: ShieldResponse) -> None:
        if assessment.risk_level in [RiskLevel.HIGH, RiskLevel.CRITICAL]:
            log_message = (
                f"[SECURITY ALERT] Transaction {assessment.transaction_id} "
                f"Flagged as {assessment.risk_level.value} | "
                f"Score: {assessment.risk_score} | "
                f"Reasons: {', '.join(assessment.reasons)}"
            )
            logger.warning(log_message)
            
            # Send webhook payload asynchronously when configured
            if self.webhook_url:
                await self._dispatch_webhook(assessment)

    async def _dispatch_webhook(self, assessment: ShieldResponse):
        # Placeholder for httpx or aiohttp async post call
        logger.info(f"Dispatched async alert webhook to {self.webhook_url}")