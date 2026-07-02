from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    environment: str = "development"

    # Schema-owning role: used by Alembic migrations (DDL) only.
    postgres_user: str = "trading_app"
    postgres_password: str = "changeme"
    # Least-privilege runtime role (created by migration 0004): DML only,
    # no UPDATE/DELETE on the append-only ledger tables. The backend
    # runtime connects as this role, never as the schema owner.
    postgres_app_user: str = "trading_runtime"
    postgres_app_password: str = "changeme"
    postgres_db: str = "trading"
    postgres_host: str = "postgres"
    postgres_port: int = 5432

    redis_host: str = "redis"
    redis_port: int = 6379

    # Symmetric key for reversible encryption of api_credentials.encrypted_value.
    # Must be a urlsafe base64-encoded 32-byte key (Fernet.generate_key()).
    credential_encryption_key: str = ""

    # HS256 signing secret for access tokens. No default on purpose —
    # token issuing/verification refuses to run without it (app/auth.py).
    jwt_secret_key: str = ""
    # Short-lived by design (scaffold-roadmap §2): the operator re-logs-in,
    # tokens are never refreshed.
    jwt_ttl_minutes: int = 30

    # The only origin the browser may call the API from (CORS pin).
    frontend_origin: str = "http://localhost:3000"

    # Failed-login limiter: after `attempts` failures for a username, the
    # login endpoint answers 429 until the window expires (Redis counter).
    login_max_failures: int = 5
    login_failure_window_seconds: int = 300

    backend_port: int = 5000

    @property
    def database_url(self) -> str:
        """Schema-owner connection — migrations and test fixtures (DDL)."""
        return (
            f"postgresql+psycopg://{self.postgres_user}:{self.postgres_password}"
            f"@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"
        )

    @property
    def app_database_url(self) -> str:
        """Runtime connection — the DML-only role the backend runs as."""
        return (
            f"postgresql+psycopg://{self.postgres_app_user}:{self.postgres_app_password}"
            f"@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"
        )


@lru_cache
def get_settings() -> Settings:
    return Settings()
