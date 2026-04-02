"""
程序入口模块
启动定时任务、初始化所有模块
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from logger_util import log_info, log_error
from config_loader import load_config
from weather_fetcher import fetch_weather_data
from data_saver import save_weather_data
from task_scheduler import run_scheduled_task


def fetch_and_save_weather(city, timeout_seconds):
    """
    获取天气数据并保存
    参数:
        city: 城市名称
        timeout_seconds: 请求超时时间（秒）
    """
    weather_data = fetch_weather_data(city, timeout_seconds)
    
    if weather_data:
        save_weather_data(weather_data)
        log_info(f"城市 {city} 的天气数据获取并保存成功")
    else:
        log_error(f"城市 {city} 的天气数据获取失败")


def main():
    """
    程序主函数
    加载配置、初始化模块、启动定时任务
    """
    log_info("=" * 50)
    log_info("天气获取小程序启动")
    log_info("=" * 50)
    
    config = load_config()
    
    if not config:
        log_error("配置加载失败，程序退出")
        sys.exit(1)
    
    city = config.get("city", "北京")
    interval_minutes = config.get("interval_minutes", 10)
    timeout_seconds = config.get("timeout_seconds", 10)
    
    log_info(f"目标城市: {city}")
    log_info(f"执行间隔: {interval_minutes} 分钟")
    log_info(f"超时时间: {timeout_seconds} 秒")
    
    try:
        run_scheduled_task(
            fetch_and_save_weather,
            interval_minutes,
            city,
            timeout_seconds
        )
    except KeyboardInterrupt:
        log_info("程序被用户中断")
    except Exception as e:
        log_error(f"程序运行异常: {e}")
    finally:
        log_info("=" * 50)
        log_info("天气获取小程序停止")
        log_info("=" * 50)


if __name__ == "__main__":
    main()
