from PySide6.QtWidgets import QWidget, QLabel, QHBoxLayout


class StatusBar(QWidget):

    def __init__(self):
        super().__init__()

        layout = QHBoxLayout(self)

        layout.addWidget(QLabel("Status : Ready"))

        layout.addStretch()

        layout.addWidget(QLabel("437.000 MHz"))