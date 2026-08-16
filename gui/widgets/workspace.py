import numpy as np
from PySide6.QtWidgets import (
    QWidget, QHBoxLayout, QVBoxLayout, QGridLayout,
    QGroupBox, QLabel, QLineEdit, QComboBox, QSlider,
    QPushButton, QProgressBar, QTextEdit
)
from PySide6.QtCore import Qt, QTimer
import pyqtgraph as pg

from gnuradio.controller import GNUController


class Workspace(QWidget):
    def __init__(self):
        super().__init__()
        self.ctrl = GNUController()

        main_layout = QHBoxLayout(self)

        # ==========================================
        # 1. پنل سمت چپ: تنظیمات RTL-SDR (Downlink Only)
        # ==========================================
        left_panel = QVBoxLayout()

        # CONNECTION
        conn_box = QGroupBox("CONNECTION")
        conn_layout = QGridLayout()

        self.dev_combo = QComboBox()
        self.dev_combo.addItems(["RTL-SDR v3/v4", "Generic RTL2832U"])
        conn_layout.addWidget(QLabel("Device:"), 0, 0)
        conn_layout.addWidget(self.dev_combo, 0, 1)

        self.sample_input = QLineEdit("2000000")
        conn_layout.addWidget(QLabel("Sample Rate:"), 1, 0)
        conn_layout.addWidget(self.sample_input, 1, 1)

        self.bw_input = QLineEdit("250000")
        conn_layout.addWidget(QLabel("Bandwidth:"), 2, 0)
        conn_layout.addWidget(self.bw_input, 2, 1)

        conn_box.setLayout(conn_layout)
        left_panel.addWidget(conn_box)

        # RECEIVER (RX)
        rx_box = QGroupBox("RECEIVER (RX)")
        rx_layout = QVBoxLayout()

        rx_layout.addWidget(QLabel("Frequency (Hz):"))
        self.freq_input = QLineEdit("437500000")
        self.freq_input.setStyleSheet("font-size: 14px; font-weight: bold; color: #4caf50;")
        rx_layout.addWidget(self.freq_input)

        rx_layout.addWidget(QLabel("Tuner Gain (dB):"))
        self.gain_slider = QSlider(Qt.Horizontal)
        self.gain_slider.setRange(0, 49)
        self.gain_slider.setValue(30)
        rx_layout.addWidget(self.gain_slider)

        rx_box.setLayout(rx_layout)
        left_panel.addWidget(rx_box)

        left_panel.addStretch()
        main_layout.addLayout(left_panel, 1)

        # ==========================================
        # 2. بخش مرکزی: Spectrum + Waterfall (در یک صفحه)
        # ==========================================
        center_panel = QVBoxLayout()

        pg.setConfigOption('background', '#151921')
        pg.setConfigOption('foreground', '#d0d4dc')

        # Spectrum Plot
        self.spectrum_plot = pg.PlotWidget(title="SPECTRUM (dBFs)")
        self.spectrum_plot.showGrid(x=True, y=True, alpha=0.3)
        self.spectrum_curve = self.spectrum_plot.plot(pen=pg.mkPen(color='#3b82f6', width=1.5))
        center_panel.addWidget(self.spectrum_plot, 1)

        # Waterfall Plot
        self.waterfall_plot = pg.PlotWidget(title="WATERFALL")
        self.waterfall_image = pg.ImageItem()
        self.waterfall_plot.addItem(self.waterfall_image)
        center_panel.addWidget(self.waterfall_plot, 1)

        main_layout.addLayout(center_panel, 3)

        # ==========================================
        # 3. پنل سمت راست: متریک‌ها، لاگ و کنترل‌ها
        # ==========================================
        right_panel = QVBoxLayout()

        # SIGNAL METRICS
        metrics_box = QGroupBox("SIGNAL METRICS")
        m_layout = QGridLayout()
        m_layout.addWidget(QLabel("RSSI:"), 0, 0)
        self.rssi_label = QLabel("-45.2 dBm")
        m_layout.addWidget(self.rssi_label, 0, 1)

        m_layout.addWidget(QLabel("Signal Level:"), 1, 0)
        self.signal_bar = QProgressBar()
        self.signal_bar.setValue(75)
        m_layout.addWidget(self.signal_bar, 1, 1)

        metrics_box.setLayout(m_layout)
        right_panel.addWidget(metrics_box)

        # CONTROL
        ctrl_box = QGroupBox("CONTROL")
        ctrl_layout = QGridLayout()

        self.start_btn = QPushButton("► Start RX")
        self.stop_btn = QPushButton("■ Stop RX")

        self.start_btn.clicked.connect(self.start_receiver)
        self.stop_btn.clicked.connect(self.stop_receiver)

        ctrl_layout.addWidget(self.start_btn, 0, 0)
        ctrl_layout.addWidget(self.stop_btn, 0, 1)

        ctrl_box.setLayout(ctrl_layout)
        right_panel.addWidget(ctrl_box)

        # LOG
        right_panel.addWidget(QLabel("System Log:"))
        self.log_box = QTextEdit()
        self.log_box.setReadOnly(True)
        right_panel.addWidget(self.log_box, 1)

        main_layout.addLayout(right_panel, 1)
        # این بخش را به پایان متد __init__ در workspace.py اضافه کنید
        self.data_buffer = np.zeros((100, 256))

        # تایمر برای بروزرسانی گرافیکی با نرخ 20 فریم بر ثانیه
        self.plot_timer = QTimer()
        self.plot_timer.timeout.connect(self.update_live_plots)

    def start_receiver(self):
        # ... کدهای قبلی ...
        self.ctrl.start()
        self.plot_timer.start(50)  # شروع بروزرسانی نمودارها هر 50 میلی‌ثانیه
        self.log_box.append(">> Receiver Started with RTL-SDR.")

    def stop_receiver(self):
        self.plot_timer.stop()
        self.ctrl.stop()
        self.log_box.append(">> Receiver Stopped.")

    def update_live_plots(self):
        # دریافت داده‌های واقعی IQ از GNU Radio یا شبیه‌سازی سیگنال در صورت عدم اتصال
        if hasattr(self.ctrl, 'get_fft_data'):
            fft_data = self.ctrl.get_fft_data()
        else:
            # ساخت سیگنال نمونه برای تست گرافیکی
            x = np.linspace(-10, 10, 256)
            noise = np.random.normal(-100, 4, 256)
            fft_data = -40 * np.exp(-x ** 2) + noise

        # 1. بروزرسانی Spectrum
        self.spectrum_curve.setData(fft_data)

        # 2. بروزرسانی Waterfall
        self.data_buffer = np.roll(self.data_buffer, -1, axis=0)
        self.data_buffer[-1, :] = fft_data
        self.waterfall_image.setImage(self.data_buffer.T, autoLevels=False, levels=[-110, -30])

    def start_receiver(self):
        # اتصال داده‌ها به GNUController موجود در پروژه شما
        freq = float(self.freq_input.text())
        srate = int(self.sample_input.text())
        gain = int(self.gain_slider.value())

        if hasattr(self.ctrl, 'set_frequency'):
            self.ctrl.set_frequency(freq)
        if hasattr(self.ctrl, 'set_sample_rate'):
            self.ctrl.set_sample_rate(srate)
        if hasattr(self.ctrl, 'set_gain'):
            self.ctrl.set_gain(gain)

        self.ctrl.start()
        self.log_box.append(">> Receiver Started with RTL-SDR.")

    def stop_receiver(self):
        self.ctrl.stop()
        self.log_box.append(">> Receiver Stopped.")