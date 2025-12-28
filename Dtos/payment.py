class Payment(BaseModel):
    amount: Decimal = Field(gt=0)
    currency: str
    bin_country: str | None = None