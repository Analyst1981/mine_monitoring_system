"""
智能报警系统模块
负责检测异常并触发相应的报警机制
"""
import time
import threading
from typing import Dict, List, Optional, Callable
from dataclasses import dataclass
from enum import Enum
from loguru import logger
from ..config.settings import ALARM_THRESHOLDS
from ..utils.database import DatabaseManager


class AlarmLevel(Enum):
    NORMAL = "normal"
    WARNING = "warning"
    DANGER = "danger"


class AlarmType(Enum):
    THRESHOLD = "threshold"
    TREND = "trend"
    ANOMALY = "anomaly"
    SYSTEM = "system"


@dataclass
class AlarmEvent:
    id: Optional[int]
    alarm_type: AlarmType
    alarm_level: AlarmLevel
    parameter_name: str
    parameter_value: float
    threshold_value: float
    message: str
    timestamp: float
    acknowledged: bool = False
    def to_dict(self) -> Dict:
        return {'id': self.id, 'alarm_type': self.alarm_type.value, 'alarm_level': self.alarm_level.value, 'parameter_name': self.parameter_name, 'parameter_value': self.parameter_value, 'threshold_value': self.threshold_value, 'message': self.message, 'timestamp': self.timestamp, 'acknowledged': self.acknowledged}


class AlarmRule:
    def __init__(self, parameter: str, thresholds: Dict):
        self.parameter = parameter
        self.normal_range = thresholds['normal']
        self.warning_range = thresholds['warning']
        self.danger_range = thresholds['danger']
    def evaluate(self, value: float) -> AlarmLevel:
        if self.danger_range[0] <= value <= self.danger_range[1] or value > self.danger_range[1]:
            return AlarmLevel.DANGER
        elif self.warning_range[0] <= value <= self.warning_range[1]:
            return AlarmLevel.WARNING
        else:
            return AlarmLevel.NORMAL


class AlarmSystem:
    def __init__(self):
        self.db_manager = DatabaseManager()
        self.alarm_rules = self._init_alarm_rules()
        self.active_alarms: Dict[str, AlarmEvent] = {}
        self.alarm_history: List[AlarmEvent] = []
        self.alarm_callbacks: List[Callable] = []
        self.alarm_suppression = {'min_interval': 60, 'max_count_per_hour': 10}
        self.alarm_stats = {'total_alarms': 0, 'alarms_today': 0, 'last_alarm_time': None}
        self.lock = threading.Lock()

    def _init_alarm_rules(self) -> Dict[str, AlarmRule]:
        rules = {}
        for param, thresholds in ALARM_THRESHOLDS.items():
            rules[param] = AlarmRule(param, thresholds)
        return rules

    # ...其余实现省略
