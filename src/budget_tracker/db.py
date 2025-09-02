"""
Database connection and SQLAlchemy metadata setup.
Creates tables on import for MVP.
Provides CRUD functions for transactions and rules.
"""

from typing import Any

from sqlalchemy import create_engine

from . import models, schemas
from .config import config

engine = create_engine(config.database_url, echo=config.app_env == "dev")

# Create all tables on import
models.meta.create_all(engine)

metadata = models.meta


def create_transaction(txn_data: schemas.TransactionCreate) -> dict[str, Any]:
    """
    Insert a new transaction into the database.
    Returns the created transaction dict.
    """
    with engine.connect() as conn:
        txn_dict = txn_data.dict()
        txn_dict["category"] = None  # will apply rules later
        txn_dict["external_txn_id"] = None  # for Plaid
        txn_insert = models.transactions.insert().values(**txn_dict)
        result = conn.execute(txn_insert)
        inserted_pk = result.inserted_primary_key
        txn_dict["id"] = inserted_pk[0] if inserted_pk else None
        return txn_dict


def get_transactions_account(account: str, limit: int = 100) -> list[dict[str, Any]]:
    """
    Get last N transactions for an account, ordered by date desc.
    """
    with engine.connect() as conn:
        query = (
            models.transactions.select()
            .where(models.transactions.c.account == account)
            .order_by(models.transactions.c.date.desc())
            .limit(limit)
        )
        rows = conn.execute(query)
        return [dict(row) for row in rows]


def get_category_rules(active: bool = True) -> list[dict[str, Any]]:
    """
    Get active category rules, ordered by priority desc.
    """
    with engine.connect() as conn:
        query = (
            models.category_rules.select()
            .where(models.category_rules.c.active == active)
            .order_by(models.category_rules.c.priority.desc())
        )
        rows = conn.execute(query)
        return [dict(row) for row in rows]


def get_default_rules() -> list[dict[str, str]]:
    """Get some default category rules for common merchants."""
    return [
        {"pattern": r"amazon|amzn", "category": "Shopping"},
        {"pattern": r"mcdonalds|starbucks|restaurants", "category": "Food"},
        {"pattern": r"shell|exxon", "category": "Transportation"},
        {"pattern": r"visa|mastercard|cash", "category": "Payment"},
    ]
