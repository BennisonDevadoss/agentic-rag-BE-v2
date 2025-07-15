import os

from pydantic import AnyHttpUrl, Field, PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict

from .constants import ENVIRONMENT_TYPE, LLM_MODEL_PROVIDERS

current_dir = os.path.dirname(os.path.abspath(__file__))
ENV_PATH = os.path.abspath(
    os.path.join(
        current_dir,
        f"../../.env.{os.getenv('ENVIRONMENT',ENVIRONMENT_TYPE.DEVELOPMENT.value)}",
    )
)


class Settings(BaseSettings):
    # model_config = SettingsConfigDict(env_file="../.env", env_file_encoding="utf-8")

    model_config = SettingsConfigDict(
        env_file=ENV_PATH,
        env_file_encoding="utf-8",
    )

    PORT: int = Field(default=4000)
    HOST: str = Field(default="localhost")
    DEBUG: bool = Field(default=True)
    LOG_LEVEL: str = Field(default="INFO")
    ENVIRONMENT: str = Field(default="development")
    BACKEND_URL: AnyHttpUrl = Field(default="http://localhost:4000")

    DATABASE_URL: PostgresDsn
    SHOW_SQL_ALCHEMY_QUERIES: bool = Field(default=True)

    ALLOWED_ORIGIN: str = Field(default="*")

    ALGORITHM: str = Field(default="HS256")
    SECRET_KEY: str = Field("secret_key", min_length=5)
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(default=30)

    MODEL_NAME: str = Field(default="gpt-4o")
    LLM_PROVIDER: str = Field(default=LLM_MODEL_PROVIDERS.OPENAI.value)
    LLM_PROVIDER_API_KEY: str = Field(min_length=15)

    LANGFUSE_HOST: str | None = Field(default=None)
    LANGFUSE_PUBLIC_KEY: str | None = Field(default=None)
    LANGFUSE_SECRET_KEY: str | None = Field(default=None)

    MILVUS_DB: str = Field(default="agentic_rag")
    MILVUS_PORT: int = Field(default=19530)
    MILVUS_HOST: str = Field(default="localhost")

    EMBEDDING_MODEL: str = Field(default="all-MiniLM-L6-v2")
    EMBEDDING_DIMENSION: str = Field("default")
    EMBEDDING_MODEL_PROVIDER: str = Field(512)

    REDIS_BASE_URL: str = Field(default="redis://localhost:6379/0")

    RECAPTCHA_SECRET_KEY: str | None = Field(default=None, min_length=5)


SETTINGS = Settings()
