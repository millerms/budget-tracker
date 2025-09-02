# Budget Tracker

A personal budget tracker app built with Streamlit, FastAPI, and Plaid integration for secure bank transaction imports. Track expenses, categorize transactions, and view analytics dashboards.

## Features

- Add transactions manually or import securely via Plaid
- Automatic categorization with customizable rules
- Monthly totals, category breakdowns, running balance
- Interactive charts with Plotly
- SQLite persistence (easy to set up, can migrate to Postgres later)

## Screenshot (Placeholder)

*Dashboard screenshot coming soon*

## Quickstart

1. Prerequisites: Python 3.11+
2. Create venv: `python3.11 -m venv .venv && source .venv/bin/activate`
3. Install deps: `python -m pip install -r requirements.txt -r requirements-dev.txt`
4. Configure env: `cp -n .env.example .env` then set `APP_SECRET_KEY` and `APP_KDF_SALT`
5. Start API:
   - `uvicorn budget_tracker.api.main:app --reload --port 8000`
6. Start UI (in second terminal):
   - `streamlit run src/budget_tracker/app/home.py`

Open UI at http://localhost:8501 and API docs at http://localhost:8000/docs

### Makefile shortcuts
- `make setup` (deps + pre-commit)  •  `make api`  •  `make ui`
- `make lint`  •  `make format`  •  `make typecheck`  •  `make test`

### Troubleshooting
- Uvicorn target must include `:app` (module:attribute)
- Set `PYTHONPATH="$PWD/src"` for src-layout imports
- Ensure venv Python is 3.11 and `pydantic-settings` is installed
- Encryption errors: set `APP_SECRET_KEY` and `APP_KDF_SALT` in `.env`



## Configuration

Copy `.env.example` to `.env` and set:

- `DATABASE_URL`: SQLite path (e.g., `sqlite:///./budget_tracker.db`)
- `APP_SECRET_KEY`: Strong secret (e.g., `openssl rand -hex 32`)
- `APP_KDF_SALT`: Random salt string (arbitrary text, not base64)
- `PLAID_CLIENT_ID` / `PLAID_SECRET`: Plaid credentials (use sandbox)
- `PLAID_ENV`: `sandbox` for development
- `PLAID_WEBHOOK_URL`: Typically `http://localhost:8000/plaid/webhook`

## Development Workflow

- Makefile (recommended): `make setup` • `make api` • `make ui` • `make lint` • `make typecheck` • `make test` • `make precommit`
- Manual: `ruff check --fix . && ruff format .` • `mypy .` • `pytest -q`

Quality gates: ruff/mypy clean; tests green.

## Roadmap

### MVP (Current)
- [x] Transaction entry form
- [x] Manual category rules and application
- [x] Dashboard: monthly totals, category breakdown, charts
- [ ] Bullets for any additional MVP features

### Phase 2: CSV Import & Budgets (Next)
- [ ] Bank CSV import with header variations
- [ ] Budget setting (monthly limits by category/account)
- [ ] Editable rules with priority and test preview
- [ ] Budget vs actual tracking

### Phase 3: Advanced Features
- [ ] Auto-categorization (basic model or rules)
- [ ] Export to CSV/Excel
- [ ] User profiles, multi-account support
- [ ] Deployment guide (Heroku/AWS/Docker)

GitHub Issues: Check the repo for Phase 2 and Phase 3 task breakdowns.

## License

MIT License
