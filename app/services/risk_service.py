from uuid import uuid4

from app.models.risk import (
    RiskCheckRequest,
    RiskCheckResponse,
    RiskDecision,
)
from app.services.rules import evaluate_rules
from app.services.scoring import (
    calculate_risk_score,
    get_risk_level,
)


class RiskService:

    def evaluate(
        self,
        request: RiskCheckRequest,
    ) -> RiskCheckResponse:

        rule_results = evaluate_rules(request)

        scores = [
            score
            for score, _ in rule_results
        ]

        reasons = [
            reason
            for _, reason in rule_results
        ]

        risk_score = calculate_risk_score(scores)

        decision = self._get_decision(risk_score)

        return RiskCheckResponse(
            request_id=str(uuid4()),
            risk_score=risk_score,
            risk_level=get_risk_level(risk_score),
            decision=decision,
            reasons=reasons,
        )

    @staticmethod
    def _get_decision(
        score: int,
    ) -> RiskDecision:

        if score >= 80:
            return RiskDecision.DECLINE

        if score >= 50:
            return RiskDecision.REVIEW

        return RiskDecision.APPROVE