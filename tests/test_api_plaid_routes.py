import pytest

pytest.importorskip("fastapi")
from fastapi.testclient import TestClient

# Support running tests without installing the package by adding 'src' to sys.path
try:  # pragma: no cover - small import guard
    from budget_tracker.api.main import app
except ModuleNotFoundError:  # fallback for IDE/test runners without src on PYTHONPATH
    import os
    import sys

    sys.path.insert(0, os.path.abspath("src"))
    from budget_tracker.api.main import app


client = TestClient(app)


def test_create_link_token() -> None:
    resp = client.post("/plaid/create_link_token", json={"user_id": "1"})
    assert resp.status_code == 200
    data = resp.json()
    assert "link_token" in data and isinstance(data["link_token"], str)
    assert data["link_token"].startswith("link-")


def test_exchange_public_token() -> None:
    payload = {"public_token": "public-sandbox-xyz"}
    resp = client.post("/plaid/exchange", json=payload)
    assert resp.status_code == 200
    data = resp.json()
    for key in ("access_token_enc", "item_id", "accounts"):
        assert key in data
    assert isinstance(data["accounts"], list)


def test_sync_transactions() -> None:
    resp = client.post("/plaid/sync", json={})
    assert resp.status_code == 200
    data = resp.json()
    for key in ("synced", "added", "modified", "removed"):
        assert key in data
    assert isinstance(data["synced"], bool)


def test_plaid_webhook() -> None:
    body = {"webhook_type": "TRANSACTIONS", "webhook_code": "SYNC_UPDATES_AVAILABLE"}
    resp = client.post("/plaid/webhook", json=body)
    assert resp.status_code == 200
    data = resp.json()
    assert data == {"ok": True}
