from pydantic_settings import BaseSettings
from pathlib import Path


class Settings(BaseSettings):
    DEBUG: bool = False
    DATABASE_URL: str = "postgresql://postgres:postgres@db:5432/licensing_db"
    LOG_LEVEL: str = "INFO"

    class Config:
        env_file = ".env"


settings = Settings()