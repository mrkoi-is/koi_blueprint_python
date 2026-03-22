from pydantic import SecretStr, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


_DEFAULT_JWT_SECRET = "change-me-to-at-least-32-characters"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_prefix="APP_",
        extra="ignore",
    )

    app_name: str = "Koi Service"
    debug: bool = False
    database_url: str = "postgresql+psycopg://postgres:postgres@localhost:5432/koi_service"
    jwt_secret: SecretStr = SecretStr(_DEFAULT_JWT_SECRET)
    redis_url: str = "redis://localhost:6379/0"
    cors_origins: list[str] = ["http://localhost:3000"]

    @model_validator(mode="after")
    def _check_jwt_secret(self) -> "Settings":
        """非 debug 模式下禁止使用默认弱密钥 / Prevent using default weak secret in production."""
        if not self.debug and self.jwt_secret.get_secret_value() == _DEFAULT_JWT_SECRET:
            raise ValueError(
                "APP_JWT_SECRET must be changed from the default value in production. "
                "Set APP_JWT_SECRET env var or enable APP_DEBUG=true for development."
            )
        return self


settings = Settings()
