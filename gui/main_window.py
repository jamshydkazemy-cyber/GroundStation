from PySide6.QtWidgets import (
    QWidget,
    QMainWindow,
    QHBoxLayout,
    QVBoxLayout,
)

from gui.widgets.sidebar import SideBar
from gui.widgets.header import Header
from gui.widgets.workspace import Workspace
from gui.widgets.page_manager import PageManager
from gui.widgets.statusbar import StatusBar


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Arcanet SDR Ground Station")
        self.resize(1400, 900)

        central = QWidget()
        self.setCentralWidget(central)

        root = QHBoxLayout(central)

        self.sidebar = SideBar()

        self.sidebar.setFixedWidth(220)

        root.addWidget(self.sidebar)

        right = QVBoxLayout()

        self.pages = PageManager()
        right.addWidget(self.pages, 1)
        self.sidebar.pageChanged.connect(
            self.pages.setCurrentIndex
        )
        right.addWidget(Header())
        right.addWidget(Workspace(), 1)
        right.addWidget(StatusBar())
        root.addLayout(right)