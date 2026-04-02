"""
统一日志管理模块
按约束写入日志文件到 ./logs/ 目录
"""
import logging
import os
from datetime import datetime

LOG_DIR = "./logs/"
LOG_FILE_PREFIX = "weather_app_"
LOG_FILE_SUFFIX = ".log"
LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


def get_logger():
    """
    获取配置好的日志记录器
    日志文件按日期命名，存储于 ./logs/ 目录
    """
    logger = logging.getLogger("weather_app")
    logger.setLevel(logging.INFO)
    
    if logger.handlers:
        return logger
    
    os.makedirs(LOG_DIR, exist_ok=True)
    
    current_date = datetime.now().strftime("%Y%m%d")
    log_file_name = f"{LOG_FILE_PREFIX}{current_date}{LOG_FILE_SUFFIX}"
    log_file_path = os.path.join(LOG_DIR, log_file_name)
    
    file_handler = logging.FileHandler(log_file_path, encoding="utf-8")
    file_handler.setLevel(logging.INFO)
    
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    
    formatter = logging.Formatter(LOG_FORMAT, datefmt=DATE_FORMAT)
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)
    
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger


def log_info(message):
    """记录 INFO 级别日志"""
    logger = get_logger()
    logger.info(message)


def log_error(message):
    """记录 ERROR 级别日志"""
    logger = get_logger()
    logger.error(message)


def log_warning(message):
    """记录 WARNING 级别日志"""
    logger = get_logger()
    logger.warning(message)


def log_debug(message):
    """记录 DEBUG 级别日志"""
    logger = get_logger()
    logger.debug(message)
