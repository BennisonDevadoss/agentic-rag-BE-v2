from typing import Callable, Any
from datetime import datetime

from config.logger import logger


def calculate_execution_time(func) -> Callable:
    def wrapper(*args, **kwargs) -> Any:
        start_time = datetime.now()
        result = func(*args, **kwargs)
        end_time = datetime.now()
        execution_time = end_time - start_time
        log_message = (
            f"Function '{func.__name__}' executed from {start_time.strftime('%Y-%m-%d %H:%M:%S')} "
            f"to {end_time.strftime('%Y-%m-%d %H:%M:%S')}, taking {execution_time} seconds."
        )
        logger.info(log_message)
        return result

    return wrapper
