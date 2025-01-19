import sys
from typing import Any

from loguru import logger

from config.models import User


def configure_activity_logger() -> None:
    logger.remove()  # Remove default handler
    logger.add(
        sys.stdout,
        level="INFO",
        format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}",
    )


def get_user_log_format(user: User) -> dict:
    return {"id": user.id, "name": user.name, "role": user.role.name}


def activity_message_format(user: User, resource_name: str, action: str) -> str:
    return f"{user.name} {action} {resource_name} successfully"


def log_activity(user: User, resource: Any, resource_name: str, action: str) -> None:
    activity_message = activity_message_format(user, resource_name, action)
    user_log_details = get_user_log_format(user)
    logger.info(
        {
            "type": "ActivityLog",
            "current_user": user_log_details,
            resource_name: resource,
        },
        activity_message,
    )


# Initialize the logger
configure_activity_logger()
