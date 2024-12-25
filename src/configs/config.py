import os
from dotenv import load_dotenv
from pydantic_settings import BaseSettings
from pathlib import Path

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent #src
TRANSLATIONS_PATH = BASE_DIR / "middleware" / "locales"
COMMANDS_PATH = BASE_DIR / "configs" / "commands.yaml"

#список директорий-языков
LANGUAGES = [d.name for d in TRANSLATIONS_PATH.iterdir() if d.is_dir()]



class Settings(BaseSettings):
    DB_USER: str = os.getenv("POSTGRES_USER")
    DB_PASSWORD: str = os.getenv("POSTGRES_PASSWORD")
    DB_HOST: str = os.getenv(
        "POSTGRES_HOST"
    )  # "localhost" - for local env # postgres for Docker
    DB_PORT: int = os.getenv("POSTGRES_PORT")
    DB_NAME: str = os.getenv("POSTGRES_DB")
    TOKEN: str = os.getenv("TOKEN")

    def get_db_url(self):
        return (
            f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}@"
            f"{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        )


settings = Settings()
