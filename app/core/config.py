from functools import lru_cache
from decimal import Decimal

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "ProcurePilot"
    app_env: str = "development"
    app_version: str = "0.0.0-dev"
    api_prefix: str = "/api/v1"
    database_url: str = "postgresql+psycopg://postgres:postgres@localhost:5432/procurepilot_ai"
    secret_key: str = "development-only-change-me-development-only-change-me-1234567890"
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    smtp_host: str | None = None
    smtp_port: int = 587
    smtp_username: str | None = None
    smtp_password: str | None = None
    smtp_use_tls: bool = True
    smtp_from_email: str | None = None
    smtp_from_name: str = "ProcurePilot"
    public_base_url: str = "http://localhost:8000"
    match_quantity_tolerance: Decimal = Decimal("0.00")
    match_price_tolerance_percent: Decimal = Decimal("0.00")
    automation_enabled: bool = True
    automation_rfq_reminder_hours: int = 24
    automation_delivery_reminder_days: int = 2
    automation_approval_reminder_hours: int = 24

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()

if settings.app_env.lower() == "production":
    if settings.secret_key.startswith("development-only-change-me"):
        raise RuntimeError("Production requires a secure SECRET_KEY.")

    if len(settings.secret_key) < 32:
        raise RuntimeError("Production SECRET_KEY must be at least 32 characters.")

    if "localhost" in settings.database_url or "127.0.0.1" in settings.database_url:
        raise RuntimeError("Production requires an external database.")
