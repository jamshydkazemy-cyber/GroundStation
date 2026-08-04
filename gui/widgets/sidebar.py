from PySide6.QtCore import Signal
from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton


class SideBar(QWidget):

    pageChanged = Signal(int)

    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)

        pages = [
            ("📡 Receiver",0),
            ("📤 Transmitter",1),
            ("📈 Spectrum",2),
            ("🌊 Waterfall",3),
            ("🛰 Telemetry",4),
            ("⚙ Settings",5)
        ]

        for text,index in pages:

            button = QPushButton(text)

            button.setMinimumHeight(45)

            button.clicked.connect(
                lambda checked=False, i=index: self.pageChanged.emit(i)
            )

            layout.addWidget(button)

        layout.addStretch()