"""Centralized settings, loaded from environment / .env."""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    llm_provider: str = "openai"
    llm_model: str = "gpt-4o-mini"
    openai_api_key: str = ""

    chroma_persist_dir: str = "./chroma_data"
    chroma_collection: str = "security_knowledge"

    api_host: str = "0.0.0.0"
    api_port: int = 8000

    langsmith_api_key: str = ""
    langsmith_project: str = "secevalagent"


settings = Settings()
