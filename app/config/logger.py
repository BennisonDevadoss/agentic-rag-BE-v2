import sys
import socket

from loguru import logger as logging

# from loguru import Logger

from .settings import SETTINGS


def configure_logging():
    log_format = "{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}"

    # Clear default Loguru handlers
    logging.remove()

    logging.add(
        sink=sys.stdout,
        level=SETTINGS.LOG_LEVEL,
        format=log_format,
    )

    hostname = socket.gethostname()

    logger = logging.bind(hostname=hostname)

    return logger


logger = configure_logging()
