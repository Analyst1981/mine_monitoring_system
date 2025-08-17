"""
历史数据面板
用于查询和导出历史数据并绘制历史曲线
"""
from PyQt6.QtWidgets import QWidget
from loguru import logger

class HistoryPanel(QWidget):
    def __init__(self):
        super().__init__()
    def query_data(self):
        pass
    def export_data(self, filename):
        pass
