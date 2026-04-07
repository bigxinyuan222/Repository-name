import json
import os
from datetime import datetime
from typing import Any, Dict
from logger_util import get_logger

OUTPUT_DIR = "./data/output"

logger = get_logger("data_saver")


def ensure_output_dir() -> None:
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
        logger.info(f"创建输出目录: {OUTPUT_DIR}")


def generate_filename() -> str:
    date_str = datetime.now().strftime("%Y%m%d")
    return f"weather_{date_str}.json"


def save_weather_data(weather_data: Dict[str, Any]) -> bool:
    try:
        ensure_output_dir()
        
        filename = generate_filename()
        filepath = os.path.join(OUTPUT_DIR, filename)
        
        existing_data = []
        if os.path.exists(filepath):
            with open(filepath, "r", encoding="utf-8") as f:
                try:
                    existing_data = json.load(f)
                    if not isinstance(existing_data, list):
                        existing_data = []
                except json.JSONDecodeError:
                    existing_data = []
        
        record = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "data": weather_data
        }
        existing_data.append(record)
        
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(existing_data, f, ensure_ascii=False, indent=2)
        
        logger.info(f"天气数据已保存至: {filepath}")
        return True
    
    except IOError as e:
        logger.error(f"文件写入错误: {e}")
        return False
    except Exception as e:
        logger.error(f"保存数据时发生错误: {e}")
        return False
