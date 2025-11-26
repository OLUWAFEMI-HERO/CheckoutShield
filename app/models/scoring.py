def calculate_risk_score(scores: list[int]) -> int:
    return min(sum(scores), 100)


def get_risk_level(score: int) -> str:
    if score >= 80:
        return "CRITICAL"

    if score >= 50:
        return "HIGH"

    if score >= 30:
        return "MEDIUM"

    return "LOW"