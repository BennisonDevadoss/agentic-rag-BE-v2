import os

from pydantic import AnyHttpUrl, Field, PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict

current_dir = os.path.dirname(os.path.abspath(__file__))
ENV_PATH = os.path.abspath(os.path.join(current_dir, "../../.env"))


class Settings(BaseSettings):
    # model_config = SettingsConfigDict(env_file="../.env", env_file_encoding="utf-8")
    model_config = SettingsConfigDict(
        env_file=ENV_PATH,
        env_file_encoding="utf-8",
    )

    PORT: int = Field(default=4000)
    HOST: str = Field(default="localhost")
    BASE_URL: AnyHttpUrl = Field(default="http://localhost:4000")
    LOG_LEVEL: str = Field(default="INFO")
    ENVIRONMENT: str = Field(default="development")
    BACKEND_URL: AnyHttpUrl = Field(default="http://localhost:4000")

    DATABASE_URL: PostgresDsn
    SHOW_SQL_ALCHEMY_QUERIES: bool = True

    ALLOWED_ORIGIN: str = Field(default="*")

    ALGORITHM: str = "HS256"
    SECRET_KEY: str = Field("secret_key", min_length=5)
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30


SETTINGS = Settings()
