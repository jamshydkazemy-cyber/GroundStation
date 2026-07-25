from PySide6.QtWidgets import QWidget, QLabel, QHBoxLayout


class Header(QWidget):

    def __init__(self):
        super().__init__()

        layout = QHBoxLayout(self)

        title = QLabel("Neora SDR Ground Station")

        status = QLabel("🟢 Connected")

        layout.addWidget(title)

        layout.addStretch()

        layout.addWidget(status)