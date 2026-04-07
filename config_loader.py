import yaml
import os

CONFIG_DIR = "./config"
DEFAULT_CONFIG_FILE = "default.yaml"
USER_CONFIG_FILE = "config.yaml"


def load_config():
    default_config_path = os.path.join(CONFIG_DIR, DEFAULT_CONFIG_FILE)
    user_config_path = os.path.join(CONFIG_DIR, USER_CONFIG_FILE)

    with open(default_config_path, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)

    if os.path.exists(user_config_path):
        with open(user_config_path, "r", encoding="utf-8") as f:
            user_config = yaml.safe_load(f)
            if user_config:
                config.update(user_config)

    validate_config(config)
    return config


def validate_config(config):
    required_fields = ["city", "interval_minutes", "timeout_seconds"]

    for field in required_fields:
        if field not in config:
            raise ValueError(f"缺少必需的配置项: {field}")

    if not isinstance(config["city"], str) or not config["city"].strip():
        raise ValueError("城市名称必须是非空字符串")

    if not isinstance(config["interval_minutes"], int) or config["interval_minutes"] < 1:
        raise ValueError("定时执行间隔必须是大于等于1的整数")

    if not isinstance(config["timeout_seconds"], int) or config["timeout_seconds"] < 1:
        raise ValueError("超时时间必须是大于等于1的整数")
