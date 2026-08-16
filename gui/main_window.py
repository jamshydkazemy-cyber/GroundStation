from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout
from gui.widgets.header import Header
from gui.widgets.workspace import Workspace
from gui.widgets.statusbar import StatusBar
from PySide6.QtCore import Qt, QTimer
import numpy as np

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Neora SDR Ground Station (RTL-SDR Downlink)")
        self.resize(1400, 850)

        central = QWidget()
        self.setCentralWidget(central)

        layout = QVBoxLayout(central)

        # ترکیب هدر، ورک‌استپیس تک‌صفحه‌ای و استاتوس‌بار
        layout.addWidget(Header())
        layout.addWidget(Workspace(), 1)
        layout.addWidget(StatusBar())
        self.data_buffer = np.zeros((100, 256))

