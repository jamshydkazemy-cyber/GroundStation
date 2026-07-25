from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton


class SideBar(QWidget):

    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)

        buttons = [
            "📡 Receiver",
            "📤 Transmitter",
            "📈 Spectrum",
            "🌊 Waterfall",
            "🛰 Telemetry",
            "⚙ Settings"
        ]

        for text in buttons:
            btn = QPushButton(text)
            btn.setMinimumHeight(45)
            layout.addWidget(btn)

        layout.addStretch()