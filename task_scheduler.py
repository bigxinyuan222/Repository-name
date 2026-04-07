import time
import traceback
from config_loader import load_config
from weather_fetcher import fetch_weather
from data_saver import save_weather_data
from logger_util import setup_logger, log_info, log_error, log_warning


def run_task(logger, config):
    city = config["city"]
    timeout = config["timeout_seconds"]

    try:
        log_info(logger, f"开始获取 {city} 的天气数据...")
        weather_data = fetch_weather(city, timeout)
        log_info(logger, f"成功获取天气数据: {weather_data}")

        filepath = save_weather_data(weather_data)
        log_info(logger, f"天气数据已保存至: {filepath}")
        return True
    except Exception as e:
        log_error(logger, f"执行任务失败: {str(e)}")
        log_error(logger, traceback.format_exc())
        return False


def start_scheduler():
    logger = setup_logger()
    log_info(logger, "天气获取程序启动")

    try:
        config = load_config()
        log_info(logger, f"配置加载成功: {config}")
    except Exception as e:
        log_error(logger, f"配置加载失败: {str(e)}")
        log_error(logger, traceback.format_exc())
        return

    interval = config["interval_minutes"] * 60
    log_info(logger, f"定时任务设置为每 {config['interval_minutes']} 分钟执行一次")

    while True:
        try:
            run_task(logger, config)
        except Exception as e:
            log_error(logger, f"主循环异常: {str(e)}")
            log_error(logger, traceback.format_exc())

        log_info(logger, f"等待 {config['interval_minutes']} 分钟后执行下一次任务...")
        time.sleep(interval)
