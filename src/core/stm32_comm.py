"""
STM32通信模块
负责与STM32硬件串口通信，接收传感器数据
"""
import serial
import threading
import time
import json
from queue import Queue
from typing import Dict, Optional, Callable
from loguru import logger
from ..config.settings import STM32_CONFIG


class STM32Communicator:
    def __init__(self):
        self.serial_port: Optional[serial.Serial] = None
        self.is_connected = False
        self.is_running = False
        self.data_queue = Queue()
        self.receive_thread = None
        self.data_callback: Optional[Callable] = None
        self.latest_data = {'pressure': 0.0, 'temperature': 0.0, 'vibration': 0.0, 'timestamp': time.time()}

    def connect(self, port: str = None, baudrate: int = None) -> bool:
        try:
            port = port or STM32_CONFIG['port']
            baudrate = baudrate or STM32_CONFIG['baudrate']
            self.serial_port = serial.Serial(port=port, baudrate=baudrate, timeout=STM32_CONFIG['timeout'])
            self.is_connected = True
            logger.info(f"成功连接STM32设备: {port}")
            return True
        except Exception as e:
            logger.error(f"连接STM32设备失败: {e}")
            self.is_connected = False
            return False

    def disconnect(self):
        self.stop_receiving()
        if self.serial_port and self.serial_port.is_open:
            self.serial_port.close()
        self.is_connected = False
        logger.info("STM32设备连接已断开")

    # ...其余实现省略（仓库中有完整实现）
