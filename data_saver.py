import json
import os
from datetime import datetime

DATA_OUTPUT_DIR = "./data/output"
WEATHER_FILENAME_FORMAT = "weather_{date}.json"


def save_weather_data(weather_data):
    if not os.path.exists(DATA_OUTPUT_DIR):
        os.makedirs(DATA_OUTPUT_DIR, exist_ok=True)

    current_date = datetime.now().strftime("%Y%m%d")
    filename = WEATHER_FILENAME_FORMAT.format(date=current_date)
    filepath = os.path.join(DATA_OUTPUT_DIR, filename)

    all_data = []
    if os.path.exists(filepath):
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                all_data = json.load(f)
        except json.JSONDecodeError:
            all_data = []

    all_data.append(weather_data)

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(all_data, f, ensure_ascii=False, indent=2)

    return filepath
