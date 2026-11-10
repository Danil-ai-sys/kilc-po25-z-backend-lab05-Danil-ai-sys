"""Settings read from .env: the data file and the log level. (M4, lesson 13)"""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="TASKS_", env_file=".env")

    data_file: str = "tasks.json"
    log_level: str = "INFO"


settings = Settings()
