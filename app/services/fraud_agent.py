class FraudScoringAgent:
    def __init__(self):
        # In a real app, these would come from a database or environment variables
        self.high_risk_countries = ["CountryX", "CountryY"]
        self.max_amount = 5000.00

    def analyze_transaction(self, payload: dict) -> dict:
        risk_score = 0
        reasons = []

        # Rule 1: Abnormally high transaction
        if payload.get("amount", 0) > self.max_amount:
            risk_score += 50
            reasons.append("Unusually high transaction amount.")
        
        return {
            "is_safe": risk_score < 70,
            "risk_score": risk_score,
            "flagged_reasons": reasons
        }
