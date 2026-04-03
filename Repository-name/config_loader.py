"""
配置文件加载与解析模块
加载并解析 YAML 配置文件，校验配置合法性
"""
import os
import yaml
from logger_util import log_info, log_error

CONFIG_DIR = "./config/"
DEFAULT_CONFIG_FILE = "default.yaml"

MIN_INTERVAL_MINUTES = 1
MAX_INTERVAL_MINUTES = 1440
MIN_TIMEOUT_SECONDS = 1
MAX_TIMEOUT_SECONDS = 300


def load_config():
    """
    加载并解析 YAML 配置文件
    仅读取 default.yaml，禁止修改、覆盖、删除该文件
    返回配置字典，如果加载失败返回 None
    """
    config_file_path = os.path.join(CONFIG_DIR, DEFAULT_CONFIG_FILE)
    
    if not os.path.exists(config_file_path):
        log_error(f"配置文件不存在: {config_file_path}")
        return None
    
    try:
        with open(config_file_path, "r", encoding="utf-8") as file:
            config = yaml.safe_load(file)
        
        if config is None:
            log_error("配置文件为空")
            return None
        
        if not validate_config(config):
            return None
        
        log_info("配置文件加载成功")
        return config
        
    except yaml.YAMLError as e:
        log_error(f"配置文件解析失败: {e}")
        return None
    except Exception as e:
        log_error(f"读取配置文件时发生错误: {e}")
        return None


def validate_config(config):
    """
    校验配置合法性
    检查必需的配置项是否存在且值合法
    返回 True 表示配置合法，False 表示不合法
    """
    required_keys = ["city", "interval_minutes", "timeout_seconds"]
    
    for key in required_keys:
        if key not in config:
            log_error(f"配置文件中缺少必需项: {key}")
            return False
    
    city = config["city"]
    if not isinstance(city, str) or not city.strip():
        log_error("城市名称必须是非空字符串")
        return False
    
    interval_minutes = config["interval_minutes"]
    if not isinstance(interval_minutes, int):
        log_error("定时执行间隔必须是整数")
        return False
    if interval_minutes < MIN_INTERVAL_MINUTES or interval_minutes > MAX_INTERVAL_MINUTES:
        log_error(f"定时执行间隔必须在 {MIN_INTERVAL_MINUTES} 到 {MAX_INTERVAL_MINUTES} 分钟之间")
        return False
    
    timeout_seconds = config["timeout_seconds"]
    if not isinstance(timeout_seconds, int):
        log_error("接口请求超时时间必须是整数")
        return False
    if timeout_seconds < MIN_TIMEOUT_SECONDS or timeout_seconds > MAX_TIMEOUT_SECONDS:
        log_error(f"接口请求超时时间必须在 {MIN_TIMEOUT_SECONDS} 到 {MAX_TIMEOUT_SECONDS} 秒之间")
        return False
    
    return True


def get_config_value(config, key, default_value=None):
    """
    获取配置项的值
    如果配置项不存在，返回默认值
    """
    if config is None:
        return default_value
    return config.get(key, default_value)
