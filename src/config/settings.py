"""
系统配置文件
"""
import os
from pathlib import Path
PROJECT_ROOT = Path(__file__).parent.parent.parent
DATA_DIR = PROJECT_ROOT / "data"
DATABASE_DIR = DATA_DIR / "database"
LOGS_DIR = DATA_DIR / "logs"
EXPORTS_DIR = DATA_DIR / "exports"
for dir_path in [DATA_DIR, DATABASE_DIR, LOGS_DIR, EXPORTS_DIR]:
    dir_path.mkdir(exist_ok=True)
DATABASE_CONFIG = {'name': 'mine_monitoring.db', 'path': DATABASE_DIR / 'mine_monitoring.db'}
STM32_CONFIG = {'port': 'COM3', 'baudrate': 115200, 'timeout': 1, 'data_format': {'pressure': {'min': 0, 'max': 1000, 'unit': 'MPa'}, 'temperature': {'min': -40, 'max': 85, 'unit': '\u00b0C'}, 'vibration': {'min': 0, 'max': 100, 'unit': 'mm/s'}}}
DEEPSEEK_CONFIG = {'api_url': 'https://api.deepseek.com/v1/chat/completions', 'api_key': '', 'model': 'deepseek-chat', 'max_tokens': 1000, 'temperature': 0.7}
ALARM_THRESHOLDS = {'pressure': {'normal': (0, 50), 'warning': (50, 80), 'danger': (80, 100)}, 'temperature': {'normal': (10, 35), 'warning': (35, 50), 'danger': (50, 70)}, 'vibration': {'normal': (0, 20), 'warning': (20, 40), 'danger': (40, 60)}}
UI_CONFIG = {'window_size': (1400, 900), 'min_window_size': (1200, 800), 'theme': 'dark', 'update_interval': 1000, 'chart_points': 100, 'language': 'zh_CN'}
LOGGING_CONFIG = {'level': 'INFO', 'format': '{time:YYYY-MM-DD HH:mm:ss} | {level} | {name} | {message}', 'rotation': '10 MB', 'retention': '30 days', 'file_path': LOGS_DIR / 'mine_monitoring.log'}
