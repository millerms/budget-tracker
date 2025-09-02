"""FastAPI application exposing Plaid-related endpoints (stubbed).

This module defines the REST API surface for Plaid integration so the
Streamlit UI never handles secrets. Endpoints are minimal stubs that
establish request/response contracts and can be wired to real Plaid
logic in later increments.
"""

import secrets

from fastapi import FastAPI
from fastapi.responses import JSONResponse

from ..schemas import (
    ExchangePublicTokenRequest,
    ExchangePublicTokenResponse,
    LinkTokenRequest,
    LinkTokenResponse,
)

app = FastAPI(title="Budget Tracker API", version="0.1.0")


@app.post(
    "/plaid/create_link_token",
    response_model=LinkTokenResponse,
)  # type: ignore[misc]
def create_link_token(_: LinkTokenRequest) -> LinkTokenResponse:
    """Return a short-lived Plaid Link token (stub).

    In production, this should call Plaid's `/link/token/create` using
    server-side credentials, never exposing secrets to the client.
    """

    token = f"link-sandbox-{secrets.token_urlsafe(16)}"
    return LinkTokenResponse(link_token=token)


@app.post(
    "/plaid/exchange",
    response_model=ExchangePublicTokenResponse,
)  # type: ignore[misc]
def exchange_public_token(
    payload: ExchangePublicTokenRequest,
) -> ExchangePublicTokenResponse:
    """Exchange a public token for an access token (stub).

    This stub returns placeholder values. A later increment will
    encrypt the access token and persist the Plaid item/accounts.
    """

    _ = payload.public_token  # acknowledged but unused in stub
    return ExchangePublicTokenResponse(
        access_token_enc="enc_dummy_token",
        item_id="item_dummy",
        accounts=[],
    )


@app.post("/plaid/sync")  # type: ignore[misc]
def sync_transactions() -> JSONResponse:
    """Trigger a cursored sync of transactions (stub)."""

    return JSONResponse(
        {
            "synced": True,
            "added": 0,
            "modified": 0,
            "removed": 0,
        }
    )


@app.post("/plaid/webhook")  # type: ignore[misc]
def plaid_webhook(_: dict[str, object]) -> JSONResponse:
    """Handle Plaid webhook events (stub)."""

    return JSONResponse({"ok": True})
