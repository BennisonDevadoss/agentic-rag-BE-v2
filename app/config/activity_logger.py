import json
from typing import Any

from config.models import User
from config.logger import logger


def get_user_log_format(user: User) -> dict:
    return {"id": user.id, "name": user.first_name, "role": user.role.name}


def activity_message_format(user: User, resource_name: str, action: str) -> str:
    return f"{user.first_name} {action} {resource_name} successfully"


def log_activity(user: User, resource: Any, resource_name: str, action: str) -> None:
    activity_message = activity_message_format(user, resource_name, action)
    user_log_details = get_user_log_format(user)
    logger.info(
        json.dumps(
            {
                "type": "ActivityLog",
                "current_user": user_log_details,
                resource_name: resource,
            }
        ),
        activity_message,
    )
