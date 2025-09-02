"""Configuration settings for the Budget Tracker app."""

from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
    """Application configuration loaded from environment variables."""

    # Pydantic v2 settings configuration
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        arbitrary_types_allowed=True,
    )

    database_url: str = "sqlite:///./budget_tracker.db"

    app_env: str = "dev"

    # Do NOT hardcode real secrets in source; set via .env
    app_secret_key: str = "changeme"  # required for encryption
    app_kdf_salt: str = "dev_salt_change_me"  # raw KDF salt bytes source

    # Holder for runtime Fernet instance; set after instantiation
    fernet: Fernet | None = None

    plaid_client_id: str = ""

    plaid_secret: str = ""

    plaid_env: str = "sandbox"

    plaid_redirect_uri: str | None = "http://localhost:8501"

    plaid_products: str = "transactions"

    plaid_country_codes: str = "US,CA"

    plaid_webhook_url: str = "http://localhost:8000/plaid/webhook"


config = Config()


def get_fernet_key(secret_key: str, salt: bytes | None = None) -> bytes:
    """Derive a Fernet-compatible key from secret key."""

    if not secret_key or secret_key == "changeme":
        raise ValueError("Set APP_SECRET_KEY to a secure value")

    # Use provided salt or configured salt (raw bytes).
    salt = salt if salt is not None else config.app_kdf_salt.encode("utf-8")

    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
    )

    derived_key = kdf.derive(secret_key.encode())

    import base64 as _b64

    return _b64.urlsafe_b64encode(derived_key)


config.fernet = Fernet(get_fernet_key(config.app_secret_key))
