from dataclasses import dataclass

from app.models.signals import RiskSignal


@dataclass(frozen=True)
class RiskAssessment:
    score: int
    level: str
    signals: list[RiskSignal]