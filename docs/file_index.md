# File Index

This is the "file card" document for budget-tracker. Each file gets a short card with purpose, inputs/outputs, key logic, and testing ideas.

Add file cards here as files are created or modified. For example:

### 📌 src/budget_tracker/config.py
⚙️ Inputs: Environment variables from .env
💡 Key Logic: Uses Pydantic to validate and provide typed config; derives Fernet key for Plaid token encryption
🧪 Testing ideas: Test missing env variables raise errors, test key derivation deterministic

### 📌 src/budget_tracker/db.py
⚙️ Inputs: database_url from config
💡 Key Logic: SQLAlchemy engine creation, metadata for table definitions
🧪 Testing: Integration test connection succeeds, test table creation from models

### 📌 src/budget_tracker/models.py
⚙️ Inputs: SQLAlchemy metadata
💡 Key Logic: Table definitions for transactions, rules, Plaid entities; indexes for performance
🧪 Testing: Test table creation, check constraints, unique indexes

### 📌 src/budget_tracker/schemas.py
⚙️ Inputs: User input JSON, table results
💡 Key Logic: Pydantic validation for API I/O, with defaults and type conversion
🧪 Testing: Test valid/invalid inputs, edge cases (empty strings, large numbers)

### 📌 src/budget_tracker/categorize.py
⚙️ Inputs: Rules list, transaction merchant/description
💡 Key Logic: Apply rules by priority, substring/regex matching, assign category if match
🧪 Testing: Unit tests for rule application, priority ordering, deterministic outcomes

### 📌 src/budget_tracker/analytics.py
⚙️ Inputs: DF of transactions, date range, account filter
💡 Key Logic: Pandas groupby for totals, KPIs; handle positive/negative amounts
🧪 Testing: Mock DF inputs, test KPIs, edge cases (no data, single transaction)

### 📌 src/budget_tracker/charts.py
⚙️ Inputs: Aggregated data from analytics
💡 Key Logic: Plotly chart builds for category breakdown, time series
🧪 Testing: Mock data inputs, check chart objects have required properties

### 📌 src/budget_tracker/io_csv.py
⚙️ Inputs: CSV file path, headers for institution types
💡 Key Logic: Pandas parsing with flexible headers, date/amount cleanup, duplicate detection
🧪 Testing: Test various CSV formats, validation errors, duplicate handling

### 📌 src/budget_tracker/utils.py
⚙️ Inputs: Date strings, amounts
💡 Key Logic: Normalization functions (capitalize strings, format currency)
🧪 Testing: Unit tests for date parsing, formatting consistency

(Add more as files are created)
