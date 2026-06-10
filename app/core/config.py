from pathlib import Path

from pydantic import AliasChoices, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


BASE_DIR = Path(__file__).resolve().parents[2]
ENV_FILE = BASE_DIR / ".env"


class Settings(BaseSettings):
    database_url: str = "sqlite:///./esera.db"
    secret_key: str = "change-me-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 60 * 24 * 7
    public_base_url: str = "http://api.esera.works"
    upload_dir: Path = BASE_DIR / "uploads"
    gemini_api_key: str = ""
    translation_model: str = Field(
        default="gemini-2.5-flash",
        validation_alias=AliasChoices("TRANSLATION_MODEL", "MODEL"),
    )
    translation_timeout_seconds: float = Field(
        default=60.0,
        validation_alias=AliasChoices("TRANSLATION_TIMEOUT_SECONDS", "TIMEOUT_SECONDS"),
    )
    ai_model: str = Field(
        default="gemini-2.5-flash",
        validation_alias=AliasChoices("AI_MODEL", "MODEL"),
    )
    summarize_timeout_seconds: float = Field(
        default=60.0,
        validation_alias=AliasChoices("SUMMARIZE_TIMEOUT_SECONDS", "TIMEOUT_SECONDS"),
    )

    model_config = SettingsConfigDict(env_file=ENV_FILE, extra="ignore")


settings = Settings()
