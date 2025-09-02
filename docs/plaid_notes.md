Use FastAPI backend (uvicorn) for Plaid. Endpoints:
- POST /plaid/create_link_token -> {link_token}
- POST /plaid/exchange {public_token} -> store encrypted access_token
- POST /plaid/sync -> cursored txns; upsert by external_txn_id
- POST /plaid/webhook -> handle TRANSACTIONS.*; trigger targeted sync

Models: institutions, plaid_items (access_token_enc), accounts, plaid_cursors, transactions(+plaid_account_id, external_txn_id unique).
Security: cryptography.Fernet with key derived from APP_SECRET_KEY; never expose PLAID_SECRET to Streamlit; dev-only token on /plaid/sync.

.env.example add:
PLAID_CLIENT_ID=...
PLAID_SECRET=...
PLAID_ENV=sandbox
PLAID_PRODUCTS=transactions
PLAID_COUNTRY_CODES=US,CA
PLAID_WEBHOOK_URL=http://localhost:8000/plaid/webhook
APP_SECRET_KEY=change_me
DATABASE_URL=sqlite:///./budget_tracker.db