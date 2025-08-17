"""
辅助函数模块
提供各种实用工具函数
"""
import time
import json
import hashlib
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional, Union
from pathlib import Path


def timestamp_to_datetime(timestamp: float) -> datetime:
    return datetime.fromtimestamp(timestamp)


def datetime_to_timestamp(dt: datetime) -> float:
    return dt.timestamp()


def format_timestamp(timestamp: float, format_str: str = "%Y-%m-%d %H:%M:%S") -> str:
    return datetime.fromtimestamp(timestamp).strftime(format_str)


def safe_float(value: Any, default: float = 0.0) -> float:
    try:
        return float(value)
    except (ValueError, TypeError):
        return default


def calculate_moving_average(data: List[float], window_size: int = 5) -> List[float]:
    if len(data) < window_size:
        return data
    result = []
    for i in range(len(data)):
        if i < window_size - 1:
            result.append(data[i])
        else:
            window_data = data[i - window_size + 1:i + 1]
            avg = sum(window_data) / len(window_data)
            result.append(avg)
    return result


def detect_anomalies(data: List[float], threshold: float = 2.0) -> List[int]:
    if len(data) < 3:
        return []
    mean = sum(data) / len(data)
    variance = sum((x - mean) ** 2 for x in data) / len(data)
    std_dev = variance ** 0.5
    anomalies = []
    for i, value in enumerate(data):
        if abs(value - mean) > threshold * std_dev:
            anomalies.append(i)
    return anomalies
