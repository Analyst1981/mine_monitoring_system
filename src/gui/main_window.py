"""
主窗口界面
矿井智能监测系统的主界面实现
"""
import sys
from PyQt6.QtWidgets import QApplication
try:
    from .monitoring_panel import MonitoringPanel
    from .analysis_panel import AnalysisPanel
    from .history_panel import HistoryPanel
    from .alarm_panel import AlarmPanel
except ImportError:
    # fallback minimal stubs
    class MonitoringPanel:
        pass
    class AnalysisPanel:
        pass
    class HistoryPanel:
        pass
    class AlarmPanel:
        pass

from ..config.settings import UI_CONFIG


def run_gui(monitoring_system=None):
    app = QApplication(sys.argv)
    main_window = None
    try:
        from PyQt6.QtWidgets import QMainWindow
        main_window = QMainWindow()
        main_window.setWindowTitle("矿井智能监测系统")
        main_window.show()
        sys.exit(app.exec())
    except Exception as e:
        print(f"启动GUI失败: {e}")

if __name__ == "__main__":
    run_gui()
