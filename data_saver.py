import json
import os
from datetime import datetime
from typing import Dict, Any

from logger_util import get_logger

OUTPUT_DIR = "./data/output"

logger = get_logger()


def save_weather_data(weather_data: Dict[str, Any]) -> bool:
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
        logger.info(f"Created output directory: {OUTPUT_DIR}")
    
    today = datetime.now().strftime("%Y%m%d")
    filename = f"weather_{today}.json"
    file_path = os.path.join(OUTPUT_DIR, filename)
    
    existing_data = []
    if os.path.exists(file_path):
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                existing_data = json.load(f)
                if not isinstance(existing_data, list):
                    existing_data = [existing_data]
        except (json.JSONDecodeError, IOError) as e:
            logger.warning(f"Failed to read existing data, will create new file: {e}")
            existing_data = []
    
    existing_data.append(weather_data)
    
    try:
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(existing_data, f, ensure_ascii=False, indent=2)
        logger.info(f"Weather data saved to: {file_path}")
        return True
    except IOError as e:
        logger.error(f"Failed to save weather data: {e}")
        return False


def format_weather_output(weather_data: Dict[str, Any]) -> str:
    output_lines = [
        f"城市: {weather_data.get('city', 'N/A')}",
        f"温度: {weather_data.get('temperature', 'N/A')}°C",
        f"天气: {weather_data.get('weather_condition', 'N/A')}",
        f"湿度: {weather_data.get('humidity', 'N/A')}%",
        f"风向: {weather_data.get('wind_direction', 'N/A')}",
        f"风速: {weather_data.get('wind_speed', 'N/A')} km/h",
        f"更新时间: {weather_data.get('update_time', 'N/A')}",
        f"获取时间: {weather_data.get('fetch_time', 'N/A')}"
    ]
    return "\n".join(output_lines)
