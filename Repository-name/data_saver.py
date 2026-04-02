"""
天气数据格式化与存储模块
格式化天气数据，按约束写入指定路径的 JSON 文件
"""
import os
import json
from datetime import datetime
from logger_util import log_info, log_error

OUTPUT_DIR = "./data/output/"
FILE_PREFIX = "weather_"
FILE_SUFFIX = ".json"


def save_weather_data(weather_data):
    """
    将天气数据保存为 JSON 文件
    文件名格式：weather_YYYYMMDD.json
    参数:
        weather_data: 天气数据字典
    返回:
        保存成功返回 True，失败返回 False
    """
    if not weather_data:
        log_error("天气数据为空，无法保存")
        return False
    
    try:
        os.makedirs(OUTPUT_DIR, exist_ok=True)
        
        current_date = datetime.now().strftime("%Y%m%d")
        file_name = f"{FILE_PREFIX}{current_date}{FILE_SUFFIX}"
        file_path = os.path.join(OUTPUT_DIR, file_name)
        
        existing_data = load_existing_data(file_path)
        
        record = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "data": weather_data
        }
        
        existing_data.append(record)
        
        with open(file_path, "w", encoding="utf-8") as file:
            json.dump(existing_data, file, ensure_ascii=False, indent=2)
        
        log_info(f"天气数据已保存到: {file_path}")
        return True
        
    except PermissionError:
        log_error(f"没有权限写入文件: {file_path}")
        return False
    except Exception as e:
        log_error(f"保存天气数据时发生错误: {e}")
        return False


def load_existing_data(file_path):
    """
    加载已存在的天气数据
    如果文件不存在或格式错误，返回空列表
    参数:
        file_path: 文件路径
    返回:
        已存在的数据列表
    """
    if not os.path.exists(file_path):
        return []
    
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)
            if isinstance(data, list):
                return data
            else:
                log_error("现有数据文件格式错误，将创建新数据")
                return []
    except json.JSONDecodeError:
        log_error("现有数据文件 JSON 解析错误，将创建新数据")
        return []
    except Exception as e:
        log_error(f"读取现有数据时发生错误: {e}")
        return []


def format_weather_for_display(weather_data):
    """
    格式化天气数据用于显示
    参数:
        weather_data: 天气数据字典
    返回:
        格式化后的字符串
    """
    if not weather_data:
        return "无天气数据"
    
    return (
        f"城市: {weather_data.get('city', 'N/A')}\n"
        f"温度: {weather_data.get('temperature_c', 'N/A')}°C\n"
        f"天气: {weather_data.get('weather_condition', 'N/A')}\n"
        f"湿度: {weather_data.get('humidity', 'N/A')}%\n"
        f"风向: {weather_data.get('wind_direction', 'N/A')}\n"
        f"风速: {weather_data.get('wind_speed_kmph', 'N/A')} km/h\n"
        f"更新时间: {weather_data.get('update_time', 'N/A')}"
    )
