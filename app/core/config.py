import os
from pydantic_settings import BaseSettings
from functools import lru_cache
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent
ENV_DIR = BASE_DIR / "env"

class Settings(BaseSettings):
    # APP
    app_name: str
    app_description: str
    app_env: str
    app_version: str
    app_docs_url: str
    app_redoc_url: str

    # AWS
    aws_access_key_id: str
    aws_secret_access_key: str
    aws_region: str
    aws_dynamodb_endpoint: str

    class Config:
        env_file = str(ENV_DIR / f".env.{os.getenv('APP_ENV', 'development')}")
        env_file_encoding = "utf-8"

@lru_cache
def get_settings():
    return Settings()
