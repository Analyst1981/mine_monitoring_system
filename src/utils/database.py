"""
数据库管理模块
负责数据的存储、查询和管理
"""
import sqlite3
import threading
from typing import List, Dict, Optional, Tuple
from datetime import datetime, timedelta
from contextlib import contextmanager
from loguru import logger
from ..config.settings import DATABASE_CONFIG


class DatabaseManager:
    def __init__(self):
        self.db_path = DATABASE_CONFIG['path']
        self.lock = threading.Lock()
        self._init_database()

    def _init_database(self):
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS sensor_data (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        pressure REAL NOT NULL,
                        temperature REAL NOT NULL,
                        vibration REAL NOT NULL,
                        timestamp REAL NOT NULL,
                        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
                    )
                ''')
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS alarm_records (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        alarm_type TEXT NOT NULL,
                        alarm_level TEXT NOT NULL,
                        parameter_name TEXT NOT NULL,
                        parameter_value REAL NOT NULL,
                        threshold_value REAL NOT NULL,
                        message TEXT,
                        timestamp REAL NOT NULL,
                        acknowledged BOOLEAN DEFAULT FALSE,
                        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
                    )
                ''')
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS system_config (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        config_key TEXT UNIQUE NOT NULL,
                        config_value TEXT NOT NULL,
                        description TEXT,
                        updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
                    )
                ''')
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS ai_analysis (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        analysis_type TEXT NOT NULL,
                        input_data TEXT NOT NULL,
                        result TEXT NOT NULL,
                        confidence REAL,
                        timestamp REAL NOT NULL,
                        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
                    )
                ''')
                cursor.execute('CREATE INDEX IF NOT EXISTS idx_sensor_timestamp ON sensor_data(timestamp)')
                conn.commit()
                logger.info("数据库初始化完成")
        except Exception as e:
            logger.error(f"数据库初始化失败: {e}")
            raise

    @contextmanager
    def get_connection(self):
        conn = None
        try:
            with self.lock:
                conn = sqlite3.connect(str(self.db_path), timeout=30.0)
                conn.row_factory = sqlite3.Row
                yield conn
        except Exception as e:
            if conn:
                conn.rollback()
            logger.error(f"数据库操作失败: {e}")
            raise
        finally:
            if conn:
                conn.close()

    def save_sensor_data(self, data: Dict) -> bool:
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO sensor_data (pressure, temperature, vibration, timestamp)
                    VALUES (?, ?, ?, ?)
                ''', (data['pressure'], data['temperature'], data['vibration'], data['timestamp']))
                conn.commit()
                return True
        except Exception as e:
            logger.error(f"保存传感器数据失败: {e}")
            return False

    # ...其余函数省略（仓库中有完整实现）
