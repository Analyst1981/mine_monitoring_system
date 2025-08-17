"""
矿井智能监测系统主程序
"""
import sys
import asyncio
from pathlib import Path
from loguru import logger

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.core.data_collector import DataCollector
from src.core.deepseek_ai import get_analyzer
from src.core.alarm_system import get_alarm_system
from src.utils.logger import setup_logger
from src.config.settings import UI_CONFIG


class MineMonitoringSystem:
    """主类"""
    def __init__(self, use_mock_data: bool = True):
        self.use_mock_data = use_mock_data
        self.data_collector = None
        self.ai_analyzer = None
        self.alarm_system = None
        self.is_running = False
        setup_logger()
        logger.info("矿井监测系统启动中...")
    
    def initialize(self):
        try:
            self.data_collector = DataCollector(use_mock=self.use_mock_data)
            self.ai_analyzer = get_analyzer()
            self.alarm_system = get_alarm_system()
            self.data_collector.subscribe(self._on_data_received)
            self.alarm_system.add_alarm_callback(self._on_alarm_triggered)
            return True
        except Exception as e:
            logger.error(f"初始化失败: {e}")
            return False
    
    def start(self, port: str = None, baudrate: int = None):
        try:
            if not self.initialize():
                return False
            if not self.data_collector.start(port, baudrate):
                logger.error("数据采集启动失败")
                return False
            self.is_running = True
            self.alarm_system.test_alarm_system()
            return True
        except Exception as e:
            logger.error(f"启动失败: {e}")
            return False
    
    def stop(self):
        try:
            self.is_running = False
            if self.data_collector:
                self.data_collector.stop()
            logger.info("系统已停止")
        except Exception as e:
            logger.error(f"停止时发生错误: {e}")
    
    def _on_data_received(self, sensor_data):
        try:
            alarms = self.alarm_system.check_sensor_data(sensor_data.to_dict())
            if alarms:
                logger.warning(f"检测到 {len(alarms)} 个报警事件")
            import time
            if hasattr(self, '_last_ai_analysis'):
                if time.time() - self._last_ai_analysis > 60:
                    asyncio.create_task(self._perform_ai_analysis(sensor_data))
                    self._last_ai_analysis = time.time()
            else:
                self._last_ai_analysis = time.time()
                asyncio.create_task(self._perform_ai_analysis(sensor_data))
        except Exception as e:
            logger.error(f"处理数据时发生错误: {e}")
    
    async def _perform_ai_analysis(self, sensor_data):
        try:
            historical_data = self.data_collector.get_recent_data(hours=1)
            historical_dict = [data.to_dict() for data in historical_data]
            safety_result = await self.ai_analyzer.analyze_safety_status(
                sensor_data.to_dict(), historical_dict
            )
            if safety_result:
                logger.info(f"AI安全分析: {safety_result.risk_level} - {safety_result.result}")
                if safety_result.risk_level in ['危险', '警告']:
                    self.alarm_system.trigger_system_alarm(
                        f"AI检测到风险: {safety_result.result}",
                        level=self.alarm_system.AlarmLevel.WARNING
                    )
        except Exception as e:
            logger.error(f"AI分析失败: {e}")
    
    def _on_alarm_triggered(self, alarm_event):
        logger.warning(f"报警触发: {alarm_event.message}")


def main():
    import argparse
    parser = argparse.ArgumentParser(description='矿井智能监测系统')
    parser.add_argument('--port', type=str)
    parser.add_argument('--baudrate', type=int, default=115200)
    parser.add_argument('--mock', action='store_true')
    parser.add_argument('--gui', action='store_true')
    args = parser.parse_args()
    system = MineMonitoringSystem(use_mock_data=args.mock)
    try:
        if args.gui:
            from src.gui.main_window import run_gui
            run_gui(system)
        else:
            if system.start(args.port, args.baudrate):
                import time
                while system.is_running:
                    time.sleep(1)
            else:
                logger.error("系统启动失败")
    except KeyboardInterrupt:
        logger.info("收到退出信号")
    except Exception as e:
        logger.error(f"运行时错误: {e}")
    finally:
        system.stop()

if __name__ == "__main__":
    main()
