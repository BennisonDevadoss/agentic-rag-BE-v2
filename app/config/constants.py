from enum import Enum


class GENERAL_CONFIGS(str, Enum):
    SESSION_COOKIE_NAME = "session_cookie"


class ENVIRONMENT_TYPE(str, Enum):
    STAGING = "staging"
    PRODUCTION = "production"
    DEVELOPMENT = "development"


class USER_ROLES(str, Enum):
    USER = "user"
    ADMIN = "admin"


class EMBEDDING_MODEL_PROVIDERS(str, Enum):
    OPENAI = "openai"
    GOOGLE = "google"
    HUGGINGFACE = "huggingface"


class LLM_MODEL_PROVIDERS(str, Enum):
    GROQ = "groq"
    OPENAI = "openai"
    GOOGLE = "google"
    ANTHROPIC = "anthropic"


class VECTOR_DB_PROVIDERS(str, Enum):
    MILVUS = "milvus"
    CHROMADB = "chromadb"
    PG_VECTOR = "pg_vector"
