from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QVBoxLayout,
    QGridLayout,
    QLineEdit,
    QPushButton,
    QComboBox,
    QProgressBar,
    QTextEdit,
)
from gnuradio.controller import GNUController


class ReceiverPage(QWidget):

    def __init__(self):
        super().__init__()
        self.ctrl = GNUController()
        self.start.clicked.connect(self.start_receiver)
        self.stop.clicked.connect(self.stop_receiver)

        main = QVBoxLayout(self)

        title = QLabel("Receiver")

        grid = QGridLayout()

        self.freq = QLineEdit("437000000")
        self.sample = QLineEdit("2000000")
        self.rfgain = QLineEdit("30")
        self.ifgain = QLineEdit("20")
        self.bandwidth = QLineEdit("250000")

        self.mode = QComboBox()
        self.mode.addItems(["FM", "AM", "USB", "LSB"])

        grid.addWidget(QLabel("Frequency"), 0, 0)
        grid.addWidget(self.freq, 0, 1)

        grid.addWidget(QLabel("Sample Rate"), 1, 0)
        grid.addWidget(self.sample, 1, 1)

        grid.addWidget(QLabel("RF Gain"), 2, 0)
        grid.addWidget(self.rfgain, 2, 1)

        grid.addWidget(QLabel("IF Gain"), 3, 0)
        grid.addWidget(self.ifgain, 3, 1)

        grid.addWidget(QLabel("Bandwidth"), 4, 0)
        grid.addWidget(self.bandwidth, 4, 1)

        grid.addWidget(QLabel("Mode"), 5, 0)
        grid.addWidget(self.mode, 5, 1)

        self.start = QPushButton("Start")
        self.stop = QPushButton("Stop")

        self.signal = QProgressBar()
        self.signal.setMaximum(100)

        self.log = QTextEdit()
        self.log.setReadOnly(True)

        main.addWidget(title)
        main.addLayout(grid)
        main.addWidget(self.start)
        main.addWidget(self.stop)
        main.addWidget(QLabel("Signal"))
        main.addWidget(self.signal)
        main.addWidget(QLabel("Log"))
        main.addWidget(self.log)

    def start_receiver(self):

        self.ctrl.set_frequency(float(self.freq.text()))

        self.ctrl.set_sample_rate(int(self.sample.text()))

        self.ctrl.set_gain(int(self.rfgain.text()))

        self.ctrl.start()

        self.log.append("Receiver Started")

    def stop_receiver(self):

        self.ctrl.stop()

        self.log.append("Receiver Stopped")