import logging
import os
from datetime import datetime

LOGS_DIR = "./logs"
LOG_FILENAME_FORMAT = "weather_{date}.log"


def setup_logger():
    if not os.path.exists(LOGS_DIR):
        os.makedirs(LOGS_DIR, exist_ok=True)

    logger = logging.getLogger("weather_fetcher")
    logger.setLevel(logging.DEBUG)
    logger.handlers.clear()

    current_date = datetime.now().strftime("%Y%m%d")
    log_filename = LOG_FILENAME_FORMAT.format(date=current_date)
    log_filepath = os.path.join(LOGS_DIR, log_filename)

    file_handler = logging.FileHandler(log_filepath, encoding="utf-8")
    file_handler.setLevel(logging.DEBUG)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)

    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger


def log_info(logger, message):
    logger.info(message)


def log_error(logger, message):
    logger.error(message)


def log_debug(logger, message):
    logger.debug(message)


def log_warning(logger, message):
    logger.warning(message)
