import time
from typing import Callable
from logger_util import get_logger

logger = get_logger("task_scheduler")


class TaskScheduler:
    def __init__(self, interval_minutes: float):
        self.interval_minutes = interval_minutes
        self.interval_seconds = interval_minutes * 60
        self.running = False
    
    def start(self, task: Callable[[], None]) -> None:
        self.running = True
        logger.info(f"定时任务启动，执行间隔: {self.interval_minutes} 分钟")
        
        while self.running:
            try:
                task()
            except Exception as e:
                logger.error(f"任务执行出错: {e}")
            
            logger.info(f"等待 {self.interval_minutes} 分钟后执行下一次任务...")
            time.sleep(self.interval_seconds)
    
    def stop(self) -> None:
        self.running = False
        logger.info("定时任务已停止")


def create_scheduler(interval_minutes: float) -> TaskScheduler:
    return TaskScheduler(interval_minutes)
