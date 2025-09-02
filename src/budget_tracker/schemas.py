"""
Pydantic schemas for Budget Tracker data validation and serialization.
"""

from pydantic import BaseModel, validator

from typing import Optional

from datetime import date

from decimal import Decimal


class TransactionCreate(BaseModel):

    """Schema for creating a new transaction."""

    date: date

    amount: Decimal  # Use Decimal for precision

    merchant: str

    description: Optional[str] = ""

    category: Optional[str] = ""

    account: str

    @validator('amount')

    def validate_amount(cls, v):

        if v <= 0:

            raise ValueError('amount must be positive')

        return v

    @validator('merchant')

    def validate_merchant(cls, v):

        return v.strip().title()


class Transaction(BaseModel):

    """Full transaction schema with ID."""

    id: int

    date: date

    amount: Decimal

    merchant: str

    description: Optional[str]

    category: Optional[str]

    account: str

    created_at: Optional[date]

    external_txn_id: Optional[str]

    plaid_account_id: Optional[str]

    class Config:

        orm_mode = True


class CategoryRuleCreate(BaseModel):

    """Schema for creating category rules."""

    pattern: str

    category: str

    priority: int = 0

    active: bool = True

    notes: Optional[str] = ""


class CategoryRule(BaseModel):

    """Full category rule schema with ID."""

    id: int

    pattern: str

    category: str

    priority: int

    active: bool

    notes: Optional[str]

    class Config:

        orm_mode = True


# Plaid DTOs
class LinkTokenRequest(BaseModel):

    user_id: Optional[str] = "1"


class LinkTokenResponse(BaseModel):

    link_token: str


class ExchangePublicTokenRequest(BaseModel):

    public_token: str


class ExchangePublicTokenResponse(BaseModel):

    access_token_enc: str

    item_id: str

    accounts: list  # stub, can extend
