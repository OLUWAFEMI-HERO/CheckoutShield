from datetime import datetime
from uuid import uuid4

from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, EmailStr, Field

from sqlalchemy import DateTime, Integer, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class RiskDecisionRecord(Base):

    __tablename__ = "risk_decisions"

    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid4()),
    )

    merchant_id: Mapped[str] = mapped_column(
        String(100),
        index=True,
    )

    checkout_id: Mapped[str] = mapped_column(
        String(100),
        index=True,
    )

    idempotency_key: Mapped[str] = mapped_column(
        String(200),
        unique=True,
        index=True,
    )

    risk_score: Mapped[int] = mapped_column(
        Integer,
    )

    decision: Mapped[str] = mapped_column(
        String(20),
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
    )


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