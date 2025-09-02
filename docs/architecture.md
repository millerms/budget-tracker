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

## Deployment & Hosting (End State)

**Goal:** A zero-install experience for you and a friend, with secure Plaid handling and minimal ops.

**UI (Streamlit Community Cloud)**
- Host the Streamlit UI on Streamlit Community Cloud for a public HTTPS URL like `https://your-app.streamlit.app`.
- Store UI-side secrets (non-Plaid) in Streamlit **Secrets Manager** and access via `st.secrets[...]`.
- Configure the UI to call the backend at `API_BASE_URL` (set in Secrets), e.g., `https://bt-backend.onrender.com`.

**Backend (FastAPI + Postgres on Render/Fly/Railway)**
- Host the FastAPI app separately (Render free tier is fine), exposing:
  - `POST /plaid/create_link_token`
  - `POST /plaid/exchange`
  - `POST /plaid/sync`
  - `POST /plaid/webhook`
  - `GET  /health`
- Environment variables managed in provider dashboard:
  - `PLAID_CLIENT_ID`, `PLAID_SECRET`, `PLAID_ENV`
  - `APP_SECRET_KEY` (used to derive Fernet key)
  - `DATABASE_URL` (Postgres)
- Optional: custom domain `api.yourdomain.com` with HTTPS.

**Database**
- Start with **Postgres (free tier)** for shared, persistent storage.
- One schema, single-role credentials stored as backend env vars.

**Security & Networking**
- Add CORS middleware in FastAPI to allow only the Streamlit Cloud origin:
  - `https://*.streamlit.app` or your exact app URL.
- Do **not** expose Plaid secrets to Streamlit. All Plaid calls remain server-side.
- Webhooks: Configure Plaid to call `https://bt-backend.onrender.com/plaid/webhook`.
- Rate limit sensitive endpoints or add a simple bearer token for `/plaid/sync` in dev.

**Secrets Management**
- UI: Streamlit Secrets Manager (`API_BASE_URL`, optional UI password, analytics keys).
- Backend: Provider env vars (`PLAID_*`, `APP_SECRET_KEY`, `DATABASE_URL`).

**Deploy Flow**
1. Push to `main` on GitHub.
2. Render auto-deploys FastAPI (health check must pass).
3. Streamlit Cloud auto-rebuilds the UI on new commits.
4. Manual smoke test: open UI → check `/health` via the UI status panel.

**Observability**
- Enable provider logs for both services.
- Add basic structured logs on sync (`added/updated/skipped/deleted` counts) and webhook events.

**Future scale knobs (if needed)**
- Migrate to Dockerized services and run both UI and API on a single platform (Render/Fly), or move to a small VPS.
- Add a lightweight auth layer (magic link or password) and per-user data partitioning.
- Introduce a job runner or cron for scheduled syncs if webhooks are insufficient.


- Type hints and Google-style docstrings
- Modular functions (<50 LOC)
- Test-driven: pytest for units, integration for end-to-end
- Clean DB migrations via Alembic (to be added)

Next: docs/roadmap.md for feature progression
