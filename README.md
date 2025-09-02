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

## Quickstart (Updated)

1. Prerequisites: Python 3.11+
2. Create venv: `python3.11 -m venv .venv && source .venv/bin/activate`
3. Install deps: `python -m pip install -r requirements.txt -r requirements-dev.txt`
4. Configure env: `cp -n .env.example .env` then set `APP_SECRET_KEY` and `APP_KDF_SALT`
5. Start API:
   - `export PYTHONPATH="$PWD/src"`
   - `python -m uvicorn budget_tracker.api.main:app --reload --port 8000`
6. Start UI:
   - `export PYTHONPATH="$PWD/src"`
   - `python -m streamlit run src/budget_tracker/app/home.py`

Open UI at http://localhost:8501 and API docs at http://localhost:8000/docs

### Makefile shortcuts
- `make setup` (deps + pre-commit)  •  `make api`  •  `make ui`
- `make lint`  •  `make format`  •  `make typecheck`  •  `make test`

### Troubleshooting
- Uvicorn target must include `:app` (module:attribute)
- Set `PYTHONPATH="$PWD/src"` for src-layout imports
- Ensure venv Python is 3.11 and `pydantic-settings` is installed
- Encryption errors: set `APP_SECRET_KEY` and `APP_KDF_SALT` in `.env`

## Quickstart

1. **Prerequisites**: Python 3.11+
2. **Clone repo**: `git clone <repo-url>`
3. **Create virtual environment**:
   ```
   python -m venv .venv
   ```
4. **Activate venv**:
   ```
   source .venv/bin/activate  # Windows: .venv\Scripts\activate
   ```
5. **Install dependencies**:
   ```
   pip install -r requirements.txt
   pip install -r requirements-dev.txt
   ```
6. **Setup configuration**:
   - Copy `.env.example` to `.env`
   - Fill in your Plaid credentials (get from Plaid dashboard, use sandbox for dev)
7. **Run the app**:
   ```
   streamlit run src/budget_tracker/app/home.py
   ```
8. **Optional: Run backend for Plaid**:
   ```
   uvicorn budget_tracker.api.main:app --reload --port 8000
   ```

Open [http://localhost:8501](http://localhost:8501) in your browser.

## Configuration

Copy `.env.example` to `.env` and set:

- `DATABASE_URL`: Path to SQLite db (e.g., `sqlite:///./budget_tracker.db`)
- `APP_SECRET_KEY`: Random string for encrypting Plaid tokens (generate via `openssl rand -hex 32`)
- `PLAID_CLIENT_ID`: Your Plaid client ID
- `PLAID_SECRET`: Your Plaid secret
- `PLAID_ENV`: `sandbox` (recommended for dev), `development`, or `production`
- Other Plaid options as needed

## Development Workflow

- **Install pre-commit**: `pre-commit install`
- **Run tests**: `pytest`
- **Check linting**: `ruff check .`
- **Format code**: `black .`
- **Type check**: `mypy src/`

Code quality gates: 85%+ test coverage for logic modules, no failing pre-commit or ruff/black checks.

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
