from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).parent.parent


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_nested_delimiter='__',
        env_file_encoding='utf-8',
        env_file=BASE_DIR / "config" / ".env"
    )

    secret_key: str | None
    mongo_url: str = "mongodb://localhost:27017/<dbname>"


settings = Settings()
