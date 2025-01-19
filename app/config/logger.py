import socket

from loguru import logger as logging

from .settings import SETTINGS


def configure_logging():
    log_format = "{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}"

    # Clear default Loguru handlers
    logging.remove()

    logging.add(
        sink="sys.stdout",
        level=SETTINGS.LOG_LEVEL,
        format=log_format,
    )

    hostname = socket.gethostname()

    logger = logging.bind(hostname=hostname)
    logger.info("this is not working")

    return logger


logger = configure_logging()
