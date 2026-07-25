from PySide6.QtWidgets import (
    QWidget,
    QMainWindow,
    QHBoxLayout,
    QVBoxLayout,
)

from gui.widgets.sidebar import SideBar
from gui.widgets.header import Header
from gui.widgets.workspace import Workspace
from gui.widgets.statusbar import StatusBar


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Arcanet SDR Ground Station")
        self.resize(1400, 900)

        central = QWidget()
        self.setCentralWidget(central)

        root = QHBoxLayout(central)

        sidebar = SideBar()
        sidebar.setFixedWidth(220)

        root.addWidget(sidebar)

        right = QVBoxLayout()

        right.addWidget(Header())
        right.addWidget(Workspace(), 1)
        right.addWidget(StatusBar())

        root.addLayout(right)