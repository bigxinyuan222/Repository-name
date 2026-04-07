import os
from typing import Any, Dict
import yaml
from logger_util import get_logger

CONFIG_DIR = "./config"
DEFAULT_CONFIG_FILE = "default.yaml"

logger = get_logger("config_loader")


def load_config(config_file: str = DEFAULT_CONFIG_FILE) -> Dict[str, Any]:
    config_path = os.path.join(CONFIG_DIR, config_file)
    
    if not os.path.exists(config_path):
        logger.error(f"配置文件不存在: {config_path}")
        raise FileNotFoundError(f"配置文件不存在: {config_path}")
    
    try:
        with open(config_path, "r", encoding="utf-8") as f:
            config = yaml.safe_load(f)
        logger.info(f"成功加载配置文件: {config_path}")
        return config
    except yaml.YAMLError as e:
        logger.error(f"配置文件格式错误: {e}")
        raise ValueError(f"配置文件格式错误: {e}")


def validate_config(config: Dict[str, Any]) -> bool:
    required_keys = ["city", "interval_minutes", "timeout_seconds"]
    
    for key in required_keys:
        if key not in config:
            logger.error(f"配置缺少必要字段: {key}")
            return False
    
    if not isinstance(config["city"], str) or not config["city"].strip():
        logger.error("配置字段 'city' 必须是非空字符串")
        return False
    
    if not isinstance(config["interval_minutes"], (int, float)) or config["interval_minutes"] <= 0:
        logger.error("配置字段 'interval_minutes' 必须是正数")
        return False
    
    if not isinstance(config["timeout_seconds"], (int, float)) or config["timeout_seconds"] <= 0:
        logger.error("配置字段 'timeout_seconds' 必须是正数")
        return False
    
    logger.info("配置校验通过")
    return True


def get_config(config_file: str = DEFAULT_CONFIG_FILE) -> Dict[str, Any]:
    config = load_config(config_file)
    
    if not validate_config(config):
        raise ValueError("配置校验失败")
    
    return config
