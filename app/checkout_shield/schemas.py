# checkout_shield/agent.py
from typing import List, Tuple
from checkout_shield.schemas import CheckoutRequest, RiskLevel, ShieldResponse

class AgenticFraudEvaluator:
    def __init__(self, max_allowed_amount: float = 2500.0, high_risk_countries: List[str] = None):
        self.max_allowed_amount = max_allowed_amount
        self.high_risk_countries = high_risk_countries or ["XX", "YY"]

    def evaluate(self, payload: CheckoutRequest) -> ShieldResponse:
        score = 0
        reasons: List[str] = []

        # Criterion 1: High Transaction Amount
        if payload.amount > self.max_allowed_amount:
            score += 35
            reasons.append(f"Transaction amount exceeds single limit limit of {self.max_allowed_amount}")

        # Criterion 2: Geographic Billing/Shipping Mismatch
        if payload.billing_country.upper() != payload.shipping_country.upper():
            score += 25
            reasons.append(f"Country mismatch: Billing ({payload.billing_country}) != Shipping ({payload.shipping_country})")

        # Criterion 3: Flagged High-Risk Jurisdiction
        if payload.shipping_country.upper() in self.high_risk_countries:
            score += 40
            reasons.append(f"Destination country {payload.shipping_country} is in the high-risk blocklist")

        # Criterion 4: Anonymous / Temporary Email Domain Check
        disposable_domains = ["tempmail.com", "throwaway.net", "mailinator.com"]
        email_domain = payload.user_email.split("@")[-1].lower()
        if email_domain in disposable_domains:
            score += 30
            reasons.append(f"Disposable email domain detected: {email_domain}")

        # Determine Risk Level and Action
        risk_level, approved, action = self._resolve_verdict(score)

        return ShieldResponse(
            transaction_id=payload.transaction_id,
            is_approved=approved,
            risk_score=score,
            risk_level=risk_level,
            reasons=reasons,
            action_recommended=action
        )

    def _resolve_verdict(self, score: int) -> Tuple[RiskLevel, bool, str]:
        if score >= 70:
            return RiskLevel.CRITICAL, False, "BLOCK_TRANSACTION"
        elif score >= 40:
            return RiskLevel.HIGH, False, "REQUIRE_3DS_VERIFICATION"
        elif score >= 20:
            return RiskLevel.MEDIUM, True, "FLAG_FOR_MANUAL_REVIEW"
        return RiskLevel.LOW, True, "ALLOW"