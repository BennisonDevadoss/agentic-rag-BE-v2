from enum import Enum


class ENVIRONMENT_TYPE(str, Enum):
    STAGING = "staging"
    PRODUCTION = "production"
    DEVELOPMENT = "development"


class USER_ROLES(str, Enum):
    USER = "user"
    ADMIN = "admin"


class EMBEDDING_MODEL_PROVIDERS(str, Enum):
    OPENAI = "openai"
    GEMINI = "gemini"
    HUGGINGFACE = "huggingface"


class LLM_MODEL_PROVIDERS(str, Enum):
    GROQ = "groq"
    OPENAI = "openai"
    GOOGLE = "google"
    ANTHROPIC = "anthropic"
