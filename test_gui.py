"""
简化的GUI测试脚本
用于测试基本界面功能
"""
import sys
from pathlib import Path
from PyQt6.QtWidgets import QApplication

from run_gui import main as run_demo

if __name__ == "__main__":
    run_demo()
