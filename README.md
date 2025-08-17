# 矿井智能监测系统

基于DeepSeek大模型和STM32的三位一体智能监测系统，用于监测矿井围压、温度和开采扰动三个关键参数。

## 系统特性

- **实时监控**: 实时显示传感器数据和状态信息
- **智能分析**: 集成DeepSeek大模型进行智能分析和预测
- **数据可视化**: 提供丰富的图表和历史数据分析
- **智能报警**: 多级报警系统和风险评估
- **历史数据**: 完整的数据存储、查询和导出功能

## 技术栈

- PyQt6 for GUI
- Pandas, NumPy, Matplotlib for data handling & plotting
- aiohttp/requests for DeepSeek API
- PySerial for STM32 communication
- SQLite for storage

## 运行

推荐使用虚拟环境并安装依赖：

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

启动 GUI:

```bash
python run_gui.py
```

命令行模式示例:

```bash
python src/main.py --mock --gui
python src/main.py --port COM3 --baudrate 115200 --gui
```

## 贡献

本项目用于学习与研究。请在 issues 提出问题或建议。
