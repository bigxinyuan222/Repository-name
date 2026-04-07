import os
from typing import Dict, Any

import yaml

from logger_util import get_logger

CONFIG_DIR = "./config"
DEFAULT_CONFIG_FILE = "default.yaml"

REQUIRED_FIELDS = ["city", "interval_minutes", "timeout_seconds"]

logger = get_logger()


def load_config(config_file: str = None) -> Dict[str, Any]:
    if config_file is None:
        config_path = os.path.join(CONFIG_DIR, DEFAULT_CONFIG_FILE)
    else:
        config_path = os.path.join(CONFIG_DIR, config_file)
    
    if not os.path.exists(config_path):
        logger.error(f"Configuration file not found: {config_path}")
        raise FileNotFoundError(f"Configuration file not found: {config_path}")
    
    try:
        with open(config_path, "r", encoding="utf-8") as f:
            config = yaml.safe_load(f)
        logger.info(f"Configuration loaded from: {config_path}")
    except yaml.YAMLError as e:
        logger.error(f"Failed to parse YAML configuration: {e}")
        raise ValueError(f"Failed to parse YAML configuration: {e}")
    
    validate_config(config)
    
    return config


def validate_config(config: Dict[str, Any]) -> None:
    if config is None:
        logger.error("Configuration is empty")
        raise ValueError("Configuration is empty")
    
    missing_fields = [field for field in REQUIRED_FIELDS if field not in config]
    if missing_fields:
        logger.error(f"Missing required configuration fields: {missing_fields}")
        raise ValueError(f"Missing required configuration fields: {missing_fields}")
    
    if not isinstance(config["city"], str) or not config["city"].strip():
        logger.error("Invalid city configuration: must be a non-empty string")
        raise ValueError("Invalid city configuration: must be a non-empty string")
    
    if not isinstance(config["interval_minutes"], (int, float)) or config["interval_minutes"] <= 0:
        logger.error("Invalid interval_minutes: must be a positive number")
        raise ValueError("Invalid interval_minutes: must be a positive number")
    
    if not isinstance(config["timeout_seconds"], (int, float)) or config["timeout_seconds"] <= 0:
        logger.error("Invalid timeout_seconds: must be a positive number")
        raise ValueError("Invalid timeout_seconds: must be a positive number")
    
    logger.info("Configuration validation passed")
