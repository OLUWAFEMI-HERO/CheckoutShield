from enum import Enum

from pydantic import BaseModel, Field


class RiskDecision(str, Enum):
    APPROVE = "APPROVE"
    REVIEW = "REVIEW"
    DECLINE = "DECLINE"


class Customer(BaseModel):
    id: str
    email: str


class Payment(BaseModel):
    amount: float = Field(gt=0)
    currency: str
    bin_country: str | None = None


class Device(BaseModel):
    id: str
    ip_address: str


class Shipping(BaseModel):
    country: str


class RiskCheckRequest(BaseModel):
    merchant_id: str
    checkout_id: str
    customer: Customer
    payment: Payment
    device: Device
    shipping: Shipping


class RiskCheckResponse(BaseModel):
    request_id: str
    risk_score: int
    risk_level: str
    decision: RiskDecision
    reasons: list[str]