from app.models.risk import RiskDecision


class DecisionEngine:

    def decide(self, score: int) -> RiskDecision:

        if score >= 80:
            return RiskDecision.DECLINE

        if score >= 50:
            return RiskDecision.REVIEW

        return RiskDecision.APPROVE