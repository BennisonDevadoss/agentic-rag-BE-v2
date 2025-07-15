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
    GEMINI = "gemini"
    HUGGINGFACE = "huggingface"


class LLM_MODEL_PROVIDERS(str, Enum):
    GROQ = "groq"
    OPENAI = "openai"
    GOOGLE = "google"
    ANTHROPIC = "anthropic"
