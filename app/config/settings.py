import os

from pydantic import AnyHttpUrl, Field, PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict

# current_dir = os.path.dirname(os.path.abspath(__file__))
# ENV_PATH = os.path.abspath(os.path.join(current_dir, "../../.env"))


class Settings(BaseSettings):
    # model_config = SettingsConfigDict(env_file="../.env", env_file_encoding="utf-8")

    model_config = SettingsConfigDict(
        env_file=f"../.env.{os.getenv('ENV', 'development')}",
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

    MILVUS_DB: str = Field(default="agentic_rag")
    MILVUS_PORT: int = Field(default=19530)
    MILVUS_HOST: str = Field(default="localhost")

    EMBEDDING_MODEL: str = Field(default="sentence-transformers/all-MiniLM-L6-v2")
    EMBEDDING_DIMENSION: str = Field("default")
    EMBEDDING_MODEL_PROVIDER: str = Field(512)


SETTINGS = Settings()
