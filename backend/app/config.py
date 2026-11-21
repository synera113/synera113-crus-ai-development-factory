from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    mode: str = "demo"
    database_url: str = "sqlite:///./crus.db"
    redis_url: str = "redis://localhost:6379/0"
    secret_key: str = "development-only-secret"
    cors_origins: str = "http://localhost:5173,http://127.0.0.1:5173"

    model_config = SettingsConfigDict(env_prefix="CRUS_", env_file=".env", extra="ignore")


settings = Settings()
