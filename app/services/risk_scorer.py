from app.models.assessment import RiskAssessment
from app.models.signals import RiskSignal


class RiskScorer:

    def calculate(
        self,
        signals: list[RiskSignal],
    ) -> RiskAssessment:

        score = min(
            sum(signal.score for signal in signals),
            100,
        )

        if score >= 80:
            level = "CRITICAL"
        elif score >= 50:
            level = "HIGH"
        elif score >= 30:
            level = "MEDIUM"
        else:
            level = "LOW"

        return RiskAssessment(
            score=score,
            level=level,
            signals=signals,
        )