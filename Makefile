.PHONY: help setup api ui lint format typecheck test precommit

PY := python
PORT ?= 8000

help:
	@echo "Targets: setup api ui lint format typecheck test precommit"
	@echo "Usage: make api PORT=8000"

setup:
	$(PY) -m pip install -U pip
	$(PY) -m pip install -r requirements.txt -r requirements-dev.txt
	pre-commit install || true

api:
	PYTHONPATH=$(PWD)/src $(PY) -m uvicorn budget_tracker.api.main:app --reload --port $(PORT)

ui:
	PYTHONPATH=$(PWD)/src $(PY) -m streamlit run src/budget_tracker/app/home.py

lint:
	ruff check --fix .
	ruff format .

format:
	ruff format .

typecheck:
	mypy .

test:
	pytest -q

precommit:
	pre-commit run --all-files

