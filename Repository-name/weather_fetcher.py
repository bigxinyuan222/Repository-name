"""
天气 API 调用与数据解析模块
调用天气 API，获取并解析原始天气数据
"""
import requests
from datetime import datetime
from logger_util import log_info, log_error, log_warning

WEATHER_API_URL = "https://wttr.in/{}?format=j1"


def fetch_weather_data(city, timeout_seconds):
    """
    调用天气 API 获取指定城市的实时天气数据
    参数:
        city: 城市名称
        timeout_seconds: 请求超时时间（秒）
    返回:
        成功返回解析后的天气数据字典，失败返回 None
    """
    url = WEATHER_API_URL.format(city)
    
    try:
        log_info(f"正在获取 {city} 的天气数据...")
        
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
        
        response = requests.get(url, headers=headers, timeout=timeout_seconds)
        response.raise_for_status()
        
        raw_data = response.json()
        parsed_data = parse_weather_data(raw_data, city)
        
        if parsed_data:
            log_info(f"成功获取 {city} 的天气数据")
            return parsed_data
        else:
            log_error(f"解析 {city} 的天气数据失败")
            return None
            
    except requests.exceptions.Timeout:
        log_error(f"请求 {city} 天气数据超时")
        return None
    except requests.exceptions.ConnectionError:
        log_error(f"网络连接错误，无法获取 {city} 的天气数据")
        return None
    except requests.exceptions.HTTPError as e:
        log_error(f"HTTP 错误: {e}")
        return None
    except requests.exceptions.RequestException as e:
        log_error(f"请求异常: {e}")
        return None
    except Exception as e:
        log_error(f"获取天气数据时发生未知错误: {e}")
        return None


def parse_weather_data(raw_data, city):
    """
    解析原始天气数据
    提取温度、天气状况、湿度、风向、更新时间等信息
    参数:
        raw_data: API 返回的原始 JSON 数据
        city: 城市名称
    返回:
        解析后的天气数据字典
    """
    try:
        if not raw_data or "current_condition" not in raw_data:
            log_error("天气数据格式错误：缺少 current_condition")
            return None
        
        current = raw_data["current_condition"][0]
        
        weather_info = {
            "city": city,
            "temperature_c": current.get("temp_C", "N/A"),
            "temperature_f": current.get("temp_F", "N/A"),
            "weather_condition": current.get("weatherDesc", [{}])[0].get("value", "N/A"),
            "humidity": current.get("humidity", "N/A"),
            "wind_direction": current.get("winddir16Point", "N/A"),
            "wind_speed_kmph": current.get("windspeedKmph", "N/A"),
            "update_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "observation_time": current.get("observation_time", "N/A")
        }
        
        return weather_info
        
    except (KeyError, IndexError, TypeError) as e:
        log_error(f"解析天气数据时发生错误: {e}")
        return None
    except Exception as e:
        log_error(f"解析天气数据时发生未知错误: {e}")
        return None


def is_city_valid(city, timeout_seconds):
    """
    检查城市名称是否有效
    参数:
        city: 城市名称
        timeout_seconds: 请求超时时间（秒）
    返回:
        城市有效返回 True，无效返回 False
    """
    url = WEATHER_API_URL.format(city)
    
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
        
        response = requests.get(url, headers=headers, timeout=timeout_seconds)
        
        if response.status_code == 200:
            data = response.json()
            if "current_condition" in data and len(data["current_condition"]) > 0:
                return True
        
        log_warning(f"城市 '{city}' 不存在或无法获取天气数据")
        return False
        
    except Exception as e:
        log_error(f"验证城市 '{city}' 时发生错误: {e}")
        return False
