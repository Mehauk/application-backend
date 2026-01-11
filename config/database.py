from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache


class DatabaseSettings(BaseSettings):
    database_url: str = ""

    model_config = SettingsConfigDict(
        env_file=(".env.example", ".env"),
    )


@lru_cache()
def get_settings():
    return DatabaseSettings()
