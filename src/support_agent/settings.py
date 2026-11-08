from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    classifier_provider: Literal["keyword", "llm"] = "keyword"
    model_name: str | None = None

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")
