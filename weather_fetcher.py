from typing import Dict, Any, Optional

import requests

from logger_util import get_logger

WTTR_API_URL = "https://wttr.in"

logger = get_logger()


def fetch_weather_data(city: str, timeout: int = 10) -> Optional[Dict[str, Any]]:
    url = f"{WTTR_API_URL}/{city}?format=j1"
    
    try:
        logger.info(f"Fetching weather data for city: {city}")
        response = requests.get(url, timeout=timeout)
        response.raise_for_status()
        
        data = response.json()
        weather_info = parse_weather_data(data, city)
        
        logger.info(f"Successfully fetched weather data for {city}")
        return weather_info
        
    except requests.exceptions.Timeout:
        logger.error(f"Request timeout while fetching weather for {city}")
        return None
    except requests.exceptions.ConnectionError:
        logger.error(f"Connection error while fetching weather for {city}")
        return None
    except requests.exceptions.HTTPError as e:
        logger.error(f"HTTP error while fetching weather for {city}: {e}")
        return None
    except requests.exceptions.RequestException as e:
        logger.error(f"Request error while fetching weather for {city}: {e}")
        return None
    except (KeyError, ValueError, TypeError) as e:
        logger.error(f"Failed to parse weather data for {city}: {e}")
        return None


def parse_weather_data(data: Dict[str, Any], city: str) -> Dict[str, Any]:
    current = data.get("current_condition", [{}])[0]
    
    weather_info = {
        "city": city,
        "temperature": current.get("temp_C", "N/A"),
        "weather_condition": current.get("weatherDesc", [{}])[0].get("value", "N/A"),
        "humidity": current.get("humidity", "N/A"),
        "wind_direction": current.get("winddir16Point", "N/A"),
        "wind_speed": current.get("windspeedKmph", "N/A"),
        "update_time": data.get("current_condition", [{}])[0].get("localObsDateTime", "N/A"),
        "fetch_time": get_current_time()
    }
    
    return weather_info


def get_current_time() -> str:
    from datetime import datetime
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
