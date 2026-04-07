import time
from typing import Callable, Dict, Any

from logger_util import get_logger

logger = get_logger()


class TaskScheduler:
    def __init__(self, interval_minutes: float):
        self.interval_minutes = interval_minutes
        self.interval_seconds = interval_minutes * 60
        self.running = False
    
    def start(self, task: Callable[[], None]) -> None:
        self.running = True
        logger.info(f"Task scheduler started with interval: {self.interval_minutes} minutes")
        
        while self.running:
            try:
                task()
            except Exception as e:
                logger.error(f"Task execution failed: {e}")
            
            if self.running:
                logger.info(f"Next execution in {self.interval_minutes} minutes...")
                time.sleep(self.interval_seconds)
    
    def stop(self) -> None:
        self.running = False
        logger.info("Task scheduler stopped")


def create_scheduler(config: Dict[str, Any]) -> TaskScheduler:
    interval = config.get("interval_minutes", 30)
    return TaskScheduler(interval)
