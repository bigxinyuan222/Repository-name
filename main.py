import sys

from config_loader import load_config
from data_saver import save_weather_data
from logger_util import setup_logger
from task_scheduler import create_scheduler
from weather_fetcher import fetch_weather_data


def main():
    logger = setup_logger()
    logger.info("=" * 50)
    logger.info("Weather Fetcher Application Starting...")
    logger.info("=" * 50)
    
    try:
        config = load_config()
    except (FileNotFoundError, ValueError) as e:
        logger.error(f"Failed to load configuration: {e}")
        sys.exit(1)
    
    city = config["city"]
    timeout = config["timeout_seconds"]
    
    def weather_task():
        logger.info(f"Executing weather fetch task for city: {city}")
        weather_data = fetch_weather_data(city, timeout)
        
        if weather_data:
            success = save_weather_data(weather_data)
            if success:
                logger.info("Weather task completed successfully")
            else:
                logger.error("Failed to save weather data")
        else:
            logger.warning("No weather data fetched, skipping save")
    
    scheduler = create_scheduler(config)
    
    try:
        scheduler.start(weather_task)
    except KeyboardInterrupt:
        logger.info("Received keyboard interrupt, shutting down...")
        scheduler.stop()
        logger.info("Application stopped gracefully")
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        scheduler.stop()
        sys.exit(1)


if __name__ == "__main__":
    main()
