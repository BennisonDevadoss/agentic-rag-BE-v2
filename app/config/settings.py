from pydantic import AnyHttpUrl, Field, PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file="../.env", env_file_encoding="utf-8")

    PORT: int = Field(default=4000)
    HOST: str = Field(default="localhost")
    BASE_URL: AnyHttpUrl = Field(default="http://localhost:4000")
    LOG_LEVEL: str = Field(default="INFO")
    ENVIRONMENT: str = Field(default="developement")
    BACKEND_URL: AnyHttpUrl = Field(default="http://localhost:4000")
    DATABASE_URL: PostgresDsn
    ALLOWED_ORIGIN: str = Field(default="*")


SETTINGS = Settings()
