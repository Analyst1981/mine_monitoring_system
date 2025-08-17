"""
日志管理模块
配置和管理系统日志
"""
import sys
from pathlib import Path
from loguru import logger
from ..config.settings import LOGGING_CONFIG


def setup_logger():
    logger.remove()
    logger.add(
        sys.stdout,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan> | <level>{message}</level>",
        level=LOGGING_CONFIG['level'],
        colorize=True
    )
    logger.add(
        LOGGING_CONFIG['file_path'],
        format=LOGGING_CONFIG['format'],
        level=LOGGING_CONFIG['level'],
        rotation=LOGGING_CONFIG['rotation'],
        retention=LOGGING_CONFIG['retention'],
        encoding='utf-8'
    )
    logger.info("日志系统初始化完成")

setup_logger()
