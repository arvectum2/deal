"""Local runtime configuration; never read provider secrets from repository files."""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="DEAL_", extra="ignore")

    host: str = "127.0.0.1"
    port: int = 8767
