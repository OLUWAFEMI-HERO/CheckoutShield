from dataclasses import dataclass


@dataclass(frozen=True)
class RiskSignal:
    code: str
    score: int
    reason: str