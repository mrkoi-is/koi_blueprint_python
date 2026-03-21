from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


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
    jwt_secret: SecretStr = SecretStr("change-me")
    redis_url: str = "redis://localhost:6379/0"
    cors_origins: list[str] = ["http://localhost:3000"]


settings = Settings()
