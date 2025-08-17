"""
GUI启动脚本
用于测试和演示矿井智能监测系统界面
"""
import sys
import os
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from src.main import MineMonitoringSystem
from src.gui.main_window import run_gui
from loguru import logger


def main():
    """主函数"""
    try:
        monitoring_system = MineMonitoringSystem(use_mock_data=True)
        logger.info("启动矿井智能监测系统GUI...")
        run_gui(monitoring_system)
    except Exception as e:
        logger.error(f"启动GUI失败: {e}")
        print(f"启动失败: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
