from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, EmailStr, Field

class RiskLevel(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"

class ItemDetail(BaseModel):
    item_id: str
    name: str
    quantity: int = Field(gt=0)
    price: float = Field(gt=0.0)

class CheckoutRequest(BaseModel):
    transaction_id: str
    user_email: EmailStr
    amount: float = Field(gt=0.0, description="Amount in local currency")
    currency: str = Field(min_length=3, max_length=3)
    ip_address: str
    billing_country: str
    shipping_country: str
    items: List[ItemDetail]

class ShieldResponse(BaseModel):
    transaction_id: str
    is_approved: bool
    risk_score: int
    risk_level: RiskLevel
    reasons: List[str]
    action_recommended: str