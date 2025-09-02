# Architecture

The Budget Tracker app is designed with a modular, scalable architecture to support gradual feature additions. It follows a source layout (`src/`) package structure for installability and clean imports.

## Tech Stack

- **Frontend**: Streamlit for web UI components and data visualization
- **Backend**: FastAPI for REST API endpoints, especially for Plaid integration
- **Database**: SQLAlchemy ORM with SQLite (easy MVP, can upgrade to Postgres)
- **APIs**: Plaid for secure bank transaction imports
- **Data Validation**: Pydantic for schema definitions and I/O validation
- **Charts**: Plotly for interactive visualizations
- **Config**: python-dotenv for environment variable management

## Component Overview

```
src/budget_tracker/
├── config.py          # Centralized settings via Pydantic Settings
├── db.py              # SQLAlchemy engine and metadata
├── models.py          # Table definitions (transactions, rules, Plaid entities)
├── schemas.py         # Pydantic models for API/request validation
├── categorize.py      # Rule application logic for transaction categorization
├── analytics.py       # Aggregation functions for balances, totals, KPIs
├── charts.py          # Plotly chart builders
├── utils.py           # Shared utilities (dates, formatting)
├── io_csv.py          # CSV import/export logic
├── plaid/             # Plaid integration layer
│   ├── client.py      # HTTP client wrapper for Plaid API
│   ├── crypto.py      # Encryption/decryption for sensitive data
│   ├── service.py     # Business logic for Plaid operations
│   └── webhook.py     # Webhook handling for sync triggers
├── api/               # FastAPI backend
│   ├── main.py        # App definition and routes
│   └── deps.py        # Shared dependencies (config, db session)
└── app/               # Streamlit pages and components
    ├── home.py        # Main dashboard with tiles and charts
    ├── add_transaction.py  # Form for manual entry
    ├── budgets.py     # Budget setup and tracking
    ├── import_csv.py  # CSV import wizard
    └── components/    # Reusable UI components (e.g., plaid_link.py)
```

## Data Model

**Transactions**
- Store all financial activity
- Fields: id, date, amount (positive/negative), merchant, description, category, account, external_txn_id
- Indexed on external_id to prevent duplicates from Plaid sync

**Category Rules**
- Regex/pattern rules for auto-categorization
- Fields: id, pattern, category, priority, active

**Plaid Entities**
- Accounts, Institutions, PlaidItems for linked banks
- Access tokens encrypted at rest

## Data Flow

1. **User Input**: Streamlit forms capture transaction data
2. **Validation**: Pydantic validates inputs before database writes
3. **Persistence**: SQLAlchemy handles ORM operations
4. **Categorization**: Apply rules on merchant/description fields
5. **Analytics**: Pandas agg on transactions for totals/balances
6. **Visualization**: Plotly builds charts from aggregated data

## Plaid Integration

To avoid exposing secrets in the browser:

- Plaid Link launches from server-generated tokens
- FastAPI backend handles all Plaid API calls
- Webhook endpoint for background syncs
- Cursor-based pagination for efficient updates

## Security

- No secrets in Streamlit (all client-side is UI-only)
- Fernet encryption for Plaid tokens using configurable key
- Input sanitization via Pydantic defenses
- dotenv for sensitive config values
- Sandbox/dev environments for testing

## Scaling Considerations

- Start with SQLite for simplicity
- Move to Postgres if needed (SQLAlchemy supports multiple DBs)
- Cache with Redis for analytics if performance becomes an issue
- FastAPI auto-scales with Uvicorn workers

## House Style

- Type hints and Google-style docstrings
- Modular functions (<50 LOC)
- Test-driven: pytest for units, integration for end-to-end
- Clean DB migrations via Alembic (to be added)

Next: docs/roadmap.md for feature progression
