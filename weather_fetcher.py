import requests
from datetime import datetime


def fetch_weather(city, timeout):
    url = f"https://wttr.in/{city}?format=j1"

    try:
        response = requests.get(url, timeout=timeout)
        response.raise_for_status()
        data = response.json()
        return parse_weather_data(data, city)
    except requests.exceptions.RequestException as e:
        raise Exception(f"请求天气API失败: {str(e)}")


def parse_weather_data(data, city):
    try:
        current = data["current_condition"][0]
        weather = {
            "city": city,
            "temperature": int(current["temp_C"]),
            "weather_condition": current["lang_zh"][0]["value"] if current.get("lang_zh") else current["weatherDesc"][0]["value"],
            "humidity": int(current["humidity"]),
            "wind_direction": current["winddir16Point"],
            "update_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        return weather
    except (KeyError, IndexError) as e:
        raise Exception(f"解析天气数据失败: {str(e)}")
