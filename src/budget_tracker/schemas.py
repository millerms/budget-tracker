"""Pydantic schemas for Budget Tracker data validation and serialization."""

import datetime
from decimal import Decimal

from pydantic import BaseModel, validator


class TransactionCreate(BaseModel):
    """Schema for creating a new transaction."""

    date: datetime.date

    amount: Decimal  # Use Decimal for precision

    merchant: str

    description: str | None = ""

    category: str | None = ""

    account: str

    @validator("amount")
    def validate_amount(cls, v: Decimal) -> Decimal:  # noqa: N805
        if v <= 0:
            raise ValueError("amount must be positive")
        return v

    @validator("merchant")
    def validate_merchant(cls, v: str) -> str:  # noqa: N805
        return v.strip().title()


class Transaction(BaseModel):
    """Full transaction schema with ID."""

    id: int

    date: datetime.date

    amount: Decimal

    merchant: str

    description: str | None

    category: str | None

    account: str

    created_at: datetime.datetime | None

    external_txn_id: str | None

    plaid_account_id: str | None

    class Config:
        orm_mode = True


class CategoryRuleCreate(BaseModel):
    """Schema for creating category rules."""

    pattern: str

    category: str

    priority: int = 0

    active: bool = True

    notes: str | None = ""


class CategoryRule(BaseModel):
    """Full category rule schema with ID."""

    id: int

    pattern: str

    category: str

    priority: int

    active: bool

    notes: str | None

    class Config:
        orm_mode = True


# Plaid DTOs
class LinkTokenRequest(BaseModel):
    user_id: str | None = "1"


class LinkTokenResponse(BaseModel):
    link_token: str


class ExchangePublicTokenRequest(BaseModel):
    public_token: str


class ExchangePublicTokenResponse(BaseModel):
    access_token_enc: str

    item_id: str

    accounts: list[dict[str, object]]
