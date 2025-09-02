"""SQLAlchemy table definitions for Budget Tracker database."""

import datetime

from sqlalchemy import (
    Boolean,
    Column,
    Date,
    DateTime,
    ForeignKey,
    Index,
    Integer,
    MetaData,
    Numeric,
    String,
    Table,
    Text,
)

# Shared metadata for all tables in this package.
meta: MetaData = MetaData()

# Plaid-related tables
institutions = Table(
    "institutions",
    meta,
    Column("id", Integer, primary_key=True, index=True),
    Column("name", String, nullable=False),
    Column("plaid_institution_id", String, unique=True, nullable=False),
)

plaid_items = Table(
    "plaid_items",
    meta,
    Column("id", Integer, primary_key=True, index=True),
    Column("plaid_item_id", String, unique=True, nullable=False),
    Column("access_token_enc", Text, nullable=False),  # encrypted access token
    Column("added_at", DateTime, nullable=False, default=datetime.datetime.utcnow),
    Column("removed", Boolean, default=False),
)

accounts = Table(
    "accounts",
    meta,
    Column("id", Integer, primary_key=True, index=True),
    Column("plaid_account_id", String, unique=True, nullable=False),
    Column("name", String, nullable=False),
    Column("mask", String),
    Column("type", String),
    Column("subtype", String),
    Column("institution_id", Integer, nullable=False),
    Column("item_id", Integer, nullable=False),
    Column("curr_balance", Numeric(precision=12, scale=2)),
    Column("curr_iso_currency", String),
    ForeignKey("institutions.id", ondelete="CASCADE"),
    ForeignKey("plaid_items.id", ondelete="CASCADE"),
)

plaid_cursors = Table(
    "plaid_cursors",
    meta,
    Column("id", Integer, primary_key=True, index=True),
    Column("item_id", Integer, nullable=False),
    Column("transactions_cursor", Text),
    Column("last_synced_at", DateTime),
    ForeignKey("plaid_items.id", ondelete="CASCADE"),
)

# Core tables
transactions = Table(
    "transactions",
    meta,
    Column("id", Integer, primary_key=True, index=True),
    Column("date", Date, nullable=False),
    # Amount is positive for income, negative for expenses.
    Column("amount", Numeric(precision=10, scale=2), nullable=False),
    Column("merchant", String, nullable=False),
    Column("description", Text),
    Column("category", String),
    # Simple account name for now.
    Column("account", String),
    # Plaid transaction ID to avoid duplicates.
    Column("external_txn_id", String, unique=True, index=True),
    Column("plaid_account_id", String, nullable=True),
    Column("created_at", DateTime, nullable=False, default=datetime.datetime.utcnow),
)

category_rules = Table(
    "category_rules",
    meta,
    Column("id", Integer, primary_key=True, index=True),
    Column("pattern", String, nullable=False),  # substring or regex pattern
    Column("category", String, nullable=False),
    Column("priority", Integer, default=0),
    Column("active", Boolean, default=True),
    Column("notes", Text),
)

# Indexes for performance
Index("idx_transactions_date", transactions.c.date)
Index("idx_transactions_category", transactions.c.category)
Index("idx_transactions_plaid_account_id", transactions.c.plaid_account_id)
Index(
    "idx_category_rules_active_priority",
    category_rules.c.active,
    category_rules.c.priority.desc(),
)
