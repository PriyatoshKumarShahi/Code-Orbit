from functools import lru_cache
from typing import List

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "SachAI"
    app_env: str = "development"
    api_v1_prefix: str = "/api/v1"
    backend_cors_origins: List[str] | str = [
        "https://code-orbit-2oly.onrender.com",
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:8000",
        "http://127.0.0.1:8000",
    ]
    backend_cors_allow_origin_regex: str | None = r"chrome-extension://.*"

    qdrant_url: str = "http://localhost:6333"
    qdrant_api_key: str | None = None
    qdrant_collection: str = "sach_claims"

    gemini_api_key: str | None = None
    gemini_model: str = "gemini-2.5-flash"

    google_search_api_key: str | None = None
    google_search_engine_id: str | None = None

    similarity_threshold: float = 0.65
    low_confidence_threshold: float = 0.6
    top_k: int = 5

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    @field_validator("backend_cors_origins", mode="before")
    @classmethod
    def parse_cors(cls, value):
        if isinstance(value, str):
            return [item.strip() for item in value.split(",") if item.strip()]
        return value


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()
