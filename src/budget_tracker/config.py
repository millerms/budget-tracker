"""Configuration settings for the Budget Tracker app."""

from pydantic_settings import BaseSettings

from typing import Optional

from cryptography.fernet import Fernet

import base64

from cryptography.hazmat.primitives import hashes

from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


class Config(BaseSettings):

    """Application configuration loaded from environment variables."""

    database_url: str = "sqlite:///./budget_tracker.db"

    app_env: str = "dev"

    app_secret_key: str = "changeme"  # required for encryption

    plaid_client_id: str = ""

    plaid_secret: str = ""

    plaid_env: str = "sandbox"

    plaid_redirect_uri: Optional[str] = "http://localhost:8501"

    plaid_products: str = "transactions"

    plaid_country_codes: str = "US,CA"

    plaid_webhook_url: str = "http://localhost:8000/plaid/webhook"

    class Config:

        env_file = ".env"

        env_file_encoding = "utf-8"

        extra = "ignore"


config = Config()


def get_fernet_key(secret_key: str) -> bytes:

    """Derive a Fernet-compatible key from secret key."""

    if not secret_key or secret_key == "changeme":

        raise ValueError("Set APP_SECRET_KEY to a secure value")

    salt = base64.urlsafe_b64decode(b'Duplicate_salt=')  # Change to random in production

    kdf = PBKDF2HMAC(

        algorithm=hashes.SHA256(),

        length=32,

        salt=salt,

        iterations=100000,

    )

    derived_key = kdf.derive(secret_key.encode())

    return base64.urlsafe_b64encode(derived_key)


config.fernet = Fernet(get_fernet_key(config.app_secret_key))
