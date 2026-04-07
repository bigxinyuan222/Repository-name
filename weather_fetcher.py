from typing import Any, Dict, Optional
import requests
from logger_util import get_logger

WTTR_API_URL = "https://wttr.in"

logger = get_logger("weather_fetcher")


def fetch_weather_data(city: str, timeout: int = 10) -> Optional[Dict[str, Any]]:
    try:
        url = f"{WTTR_API_URL}/{city}?format=j1"
        logger.info(f"正在获取城市 {city} 的天气数据")
        
        response = requests.get(url, timeout=timeout)
        response.raise_for_status()
        
        data = response.json()
        logger.info(f"成功获取城市 {city} 的天气数据")
        
        return parse_weather_data(data, city)
    
    except requests.exceptions.Timeout:
        logger.error(f"请求超时: 城市 {city}")
        return None
    except requests.exceptions.ConnectionError:
        logger.error(f"网络连接错误: 城市 {city}")
        return None
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 404:
            logger.error(f"城市不存在: {city}")
        else:
            logger.error(f"HTTP 错误: {e}")
        return None
    except requests.exceptions.RequestException as e:
        logger.error(f"请求异常: {e}")
        return None
    except KeyError as e:
        logger.error(f"数据解析错误: 缺少字段 {e}")
        return None
    except Exception as e:
        logger.error(f"未知错误: {e}")
        return None


def parse_weather_data(data: Dict[str, Any], city: str) -> Dict[str, Any]:
    current = data["current_condition"][0]
    
    weather_data = {
        "city": city,
        "temperature": current.get("temp_C", "N/A"),
        "weather_condition": current.get("weatherDesc", [{}])[0].get("value", "N/A"),
        "humidity": current.get("humidity", "N/A"),
        "wind_direction": current.get("winddir16Point", "N/A"),
        "wind_speed": current.get("windspeedKmph", "N/A"),
        "update_time": data.get("current_condition", [{}])[0].get("observation_time", "N/A"),
        "fetch_time": data.get("weather", [{}])[0].get("date", "N/A")
    }
    
    logger.debug(f"解析天气数据: {weather_data}")
    return weather_data
