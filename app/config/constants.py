from enum import Enum


class ENVIRONMENT_TYPE(str, Enum):
    TEST = "test"
    PRODUCTION = "production"
    DEVELOPMENT = "development"


class USER_ROLES(str, Enum):
    USER = "User"
    ADMIN = "Admin"
