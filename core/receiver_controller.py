from PySide6.QtCore import QObject, Signal

from sdr.rtlsdr import RTLSDR
from gnuradio.receiver import ReceiverPage


class ReceiverController(QObject):

    status_changed = Signal(str)
    frequency_changed = Signal(float)

    def __init__(self):
        super().__init__()

        self.sdr = RTLSDR()
        self.receiver = ReceiverPage()

        self.running = False

        self.frequency = 437_500_000
        self.sample_rate = 2_048_000
        self.gain = "auto"
        self.ppm = 0

    # -------------------------
    # Receiver Control
    # -------------------------

    def start(self):

        if self.running:
            return

        self.sdr.open()

        self.sdr.set_sample_rate(self.sample_rate)
        self.sdr.set_center_freq(self.frequency)
        self.sdr.set_gain(self.gain)
        self.sdr.set_ppm(self.ppm)

        self.receiver.connect_source(self.sdr)

        self.receiver.start()

        self.running = True

        self.status_changed.emit("RUNNING")

    def stop(self):

        if not self.running:
            return

        self.receiver.stop()

        self.sdr.close()

        self.running = False

        self.status_changed.emit("STOPPED")

    # -------------------------
    # Settings
    # -------------------------

    def set_frequency(self, freq):

        self.frequency = freq

        if self.running:
            self.sdr.set_center_freq(freq)

        self.frequency_changed.emit(freq)

    def set_gain(self, gain):

        self.gain = gain

        if self.running:
            self.sdr.set_gain(gain)

    def set_sample_rate(self, rate):

        self.sample_rate = rate

        if self.running:
            self.sdr.set_sample_rate(rate)

    def set_ppm(self, ppm):

        self.ppm = ppm

        if self.running:
            self.sdr.set_ppm(ppm)

    # -------------------------
    # Information
    # -------------------------

    def is_running(self):

        return self.running

    def get_frequency(self):

        return self.frequency

    def get_gain(self):

        return self.gain

    def get_sample_rate(self):

        return self.sample_rate

    def get_ppm(self):

        return self.ppm