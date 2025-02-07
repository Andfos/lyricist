from pydantic_settings import BaseSettings, SettingsConfigDict



class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    # --- Required settings even when working locally. ---

    # STANDS4
    STANDS4_ID: str = "13101"
    STANDS4_TOKEN: str | None = None

settings = Settings()