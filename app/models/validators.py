from pydantic import BaseModel, Field, field_validator


class CheckoutValidationMixin(BaseModel):

    @field_validator("merchant_id", "checkout_id")
    @classmethod
    def validate_identifier(cls, value: str) -> str:
        value = value.strip()

        if not value:
            raise ValueError("Identifier cannot be empty")

        return value