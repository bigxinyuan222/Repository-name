import sys
from logger_util import setup_logger, get_logger
from config_loader import get_config
from weather_fetcher import fetch_weather_data
from data_saver import save_weather_data
from task_scheduler import create_scheduler

logger = get_logger("main")


def weather_task(city: str, timeout: int) -> None:
    weather_data = fetch_weather_data(city, timeout)
    
    if weather_data:
        save_weather_data(weather_data)
        logger.info(f"天气数据获取成功: {weather_data['city']}")
    else:
        logger.warning(f"天气数据获取失败: {city}")


def main() -> None:
    setup_logger()
    logger.info("程序启动")
    
    try:
        config = get_config()
    except Exception as e:
        logger.error(f"配置加载失败: {e}")
        sys.exit(1)
    
    city = config["city"]
    interval_minutes = config["interval_minutes"]
    timeout = config["timeout_seconds"]
    
    logger.info(f"配置信息 - 城市: {city}, 间隔: {interval_minutes} 分钟, 超时: {timeout} 秒")
    
    scheduler = create_scheduler(interval_minutes)
    
    def task():
        weather_task(city, timeout)
    
    try:
        scheduler.start(task)
    except KeyboardInterrupt:
        logger.info("收到中断信号，程序退出")
        scheduler.stop()
    except Exception as e:
        logger.error(f"程序异常退出: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
