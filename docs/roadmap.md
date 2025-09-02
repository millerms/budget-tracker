# Roadmap

This document outlines the phased release roadmap for the Budget Tracker app. Each phase builds on the previous one, with clear milestones and acceptance criteria.

## MVP (Phase 1: Core Functionality)

*Estimated completion: Complete*

### Features
- Manual transaction entry via Streamlit form
- Basic categorization with substring-based rules (case-insensitive)
- SQLite persistence (can be upgraded to Postgres later)
- Dashboard: monthly totals, category breakdowns, running balance over time
- Configurable category rules with priority ordering
- Plotly charts for category/activity over time
- Proper type hints, docstrings, and modular code

### Acceptance Criteria
- [x] Form validation (date, amount, merchant)
- [x] Rule application deterministic and testable
- [x] KPI calculations (income, expenses, net)
- [x] Basic category pivot charts
- [x] No hardcoded paths; config-driven
- [x] Runs without errors in venv

### Technical Debt
- FastAPI shell added for Plaid wiring

## Phase 2: Import & Budgets (Next Sprint)

*Estimated start: After MVP review*

### Features
- CSV importer (robust parsing, header variations, duplicate handling)
- Budget setting (monthly limits by category/account)
- Budget vs actual reporting with warnings when exceeded
- Editable category rules form with priority and test preview
- Improved category rules: support regex patterns
- Enhanced dashboards: filters by date range, account, category
- Export current transactions to CSV
- Dark mode and responsive design for Streamlit UI

### Acceptance Criteria
- [ ] CSV import handles common formats (Chase, Wells Fargo, etc.)
- [ ] Budget tracking with visual indicators
- [ ] Rule editing interface with preview
- [ ] 85% test coverage for io_csv.py and categorize.py
- [ ] End-to-end: Import CSV → Categorize → Dashboard update

### Technical Improvements
- Alembic for database migrations
- More Pydantic validations
- Logging for tracking operations

## Phase 3: Advanced Analytics & Deployment

*Estimated start: After Phase 2*

### Features
- Auto-categorization (simple heuristic/model based on history)
- Export full reports to Excel with charts
- Multiple profiles/users (basic isolation)
- Multi-account consolidation
- Webhook support for real-time Plaid sync
- Budget alert notifications (email or in-app)
- Public demo/deployment guide

### Acceptance Criteria
- [ ] ML model achieves >85% accuracy on test set (manual classification)
- [ ] Excel export with formatted sheets and embedded charts
- [ ] Production deployment on Heroku/AWS Lambda
- [ ] Webhook integration tested with Plaid sandbox
- [ ] Multi-user: Isolation by user_id in DB

### Technical Improvements
- Docker containerization
- Redis cache for frequently accessed analytics
- Model serialization for auto-cat
- Production-grade logging/monitoring

## Known Issues & Backlog

- Issue #1: Handle timezone offsets for transaction dates
- Issue #2: Add support for recurring transactions
- Issue #3: Integration with QuickBooks/Expense apps
- Issue #4: Mobile app or responsive web design
- Issue #5: Multi-currency support

## Contributing

See CONTRIBUTING.md for development workflows and coding standards.

## Decision Log

- 09/01/2025: Confirmed Plaid integration in MVP for secure imports
- 09/01/2025: Chose Plotly over Altair for wider ecosystem support
