"""
定时任务调度模块
实现定时循环任务，控制执行频率
"""
import time
from logger_util import log_info, log_error


def run_scheduled_task(task_func, interval_minutes, *args, **kwargs):
    """
    运行定时任务
    按照指定的间隔时间循环执行任务
    参数:
        task_func: 要执行的任务函数
        interval_minutes: 执行间隔（分钟）
        *args, **kwargs: 传递给任务函数的参数
    """
    log_info(f"定时任务已启动，执行间隔: {interval_minutes} 分钟")
    
    while True:
        try:
            log_info("开始执行定时任务...")
            
            task_func(*args, **kwargs)
            
            log_info("定时任务执行完成")
            
        except Exception as e:
            log_error(f"定时任务执行时发生错误: {e}")
        
        sleep_seconds = interval_minutes * 60
        log_info(f"等待 {interval_minutes} 分钟后执行下一次任务...")
        
        try:
            time.sleep(sleep_seconds)
        except KeyboardInterrupt:
            log_info("定时任务被用户中断")
            break


def run_once(task_func, *args, **kwargs):
    """
    执行一次任务
    用于测试或手动执行
    参数:
        task_func: 要执行的任务函数
        *args, **kwargs: 传递给任务函数的参数
    返回:
        任务执行结果
    """
    try:
        log_info("执行单次任务...")
        result = task_func(*args, **kwargs)
        log_info("单次任务执行完成")
        return result
    except Exception as e:
        log_error(f"单次任务执行时发生错误: {e}")
        return None


def calculate_next_run_time(interval_minutes):
    """
    计算下次执行时间
    参数:
        interval_minutes: 执行间隔（分钟）
    返回:
        下次执行时间字符串
    """
    from datetime import datetime, timedelta
    
    next_time = datetime.now() + timedelta(minutes=interval_minutes)
    return next_time.strftime("%Y-%m-%d %H:%M:%S")
