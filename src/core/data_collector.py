"""
数据采集模块
负责数据的收集、处理和存储
"""
import time
import threading
from typing import Dict, List, Optional
from dataclasses import dataclass
from loguru import logger

from .stm32_comm import STM32Communicator, MockSTM32Communicator
from ..utils.database import DatabaseManager
from ..config.settings import STM32_CONFIG, ALARM_THRESHOLDS


@dataclass
class SensorData:
    pressure: float
    temperature: float
    vibration: float
    timestamp: float
    def to_dict(self) -> Dict:
        return {'pressure': self.pressure, 'temperature': self.temperature, 'vibration': self.vibration, 'timestamp': self.timestamp}
    @classmethod
    def from_dict(cls, data: Dict) -> 'SensorData':
        return cls(pressure=data['pressure'], temperature=data['temperature'], vibration=data['vibration'], timestamp=data['timestamp'])


class DataCollector:
    def __init__(self, use_mock: bool = False):
        self.use_mock = use_mock
        self.communicator = MockSTM32Communicator() if use_mock else STM32Communicator()
        self.db_manager = DatabaseManager()
        self.data_buffer: List[SensorData] = []
        self.buffer_lock = threading.Lock()
        self.max_buffer_size = 1000
        self.processing_thread = None
        self.is_processing = False
        self.subscribers = []
        self.stats = {'total_samples': 0, 'last_update': None, 'data_rate': 0.0, 'connection_status': False}
        self.communicator.set_data_callback(self._on_data_received)

    def start(self, port: str = None, baudrate: int = None) -> bool:
        try:
            if not self.communicator.connect(port, baudrate):
                return False
            if not self.communicator.start_receiving():
                return False
            self.is_processing = True
            self.processing_thread = threading.Thread(target=self._processing_loop)
            self.processing_thread.daemon = True
            self.processing_thread.start()
            self.stats['connection_status'] = True
            logger.info("数据采集器启动成功")
            return True
        except Exception as e:
            logger.error(f"启动失败: {e}")
            return False

    def stop(self):
        try:
            self.is_processing = False
            if self.processing_thread and self.processing_thread.is_alive():
                self.processing_thread.join(timeout=1)
            self.communicator.stop_receiving()
            self.stats['connection_status'] = False
            logger.info("数据采集器已停止")
        except Exception as e:
            logger.error(f"停止失败: {e}")

    def subscribe(self, callback):
        self.subscribers.append(callback)

    def _on_data_received(self, raw_data):
        try:
            if isinstance(raw_data, dict):
                data = SensorData.from_dict(raw_data)
            else:
                data = SensorData(pressure=raw_data.get('pressure', 0.0), temperature=raw_data.get('temperature', 0.0), vibration=raw_data.get('vibration', 0.0), timestamp=time.time())
            with self.buffer_lock:
                self.data_buffer.append(data)
                if len(self.data_buffer) > self.max_buffer_size:
                    self.data_buffer.pop(0)
                self.stats['total_samples'] += 1
                self.stats['last_update'] = data.timestamp
            self.db_manager.save_sensor_data(data.to_dict())
            for cb in self.subscribers:
                try:
                    cb(data)
                except Exception:
                    pass
        except Exception as e:
            logger.error(f"处理接收数据失败: {e}")

    def get_recent_data(self, hours: int = 1) -> List[SensorData]:
        # 返回最近 hours 小时的数据（简化）
        return list(self.data_buffer[-(hours * 60):])

    def _processing_loop(self):
        while self.is_processing:
            try:
                time.sleep(0.5)
            except Exception:
                break

    # ...其余实现省略
