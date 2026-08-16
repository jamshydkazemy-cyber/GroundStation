from __future__ import annotations

from typing import Optional, List

from PySide6.QtCore import QObject, Signal
from rtlsdr import RTLSDR
from rtlsdr import RTLSDR


class RTLSDR(QObject):

    # ---------------- Signals ----------------

    connected = Signal()
    disconnected = Signal()

    frequency_changed = Signal(int)
    gain_changed = Signal(object)
    sample_rate_changed = Signal(int)

    error = Signal(str)

    # -----------------------------------------

    def __init__(self):

        super().__init__()

        self._device: Optional[RTLSDR] = None

        self._frequency = 437_500_000
        self._sample_rate = 2_048_000
        self._gain = "auto"
        self._ppm = 0

        self._running = False

    def open(self) -> bool:

        if self._device is not None:
            return True

        try:

            self._device = RTLSDR()

            self.connected.emit()

            return True

        except Exception as e:

            self.error.emit(str(e))

            self._device = None

            return False

    def close(self):

        if self._device is None:
            return

        try:

            self._device.close()

        finally:

            self._device = None

            self.disconnected.emit()


    @property
    def is_open(self):

        return self._device is not None
    

    def set_center_freq(self, frequency: int):

        self._frequency = frequency

        if self._device:

            self._device.center_freq = frequency

        self.frequency_changed.emit(frequency)


    def set_sample_rate(self, sample_rate: int):

        self._sample_rate = sample_rate

        if self._device:

            self._device.sample_rate = sample_rate

        self.sample_rate_changed.emit(sample_rate)

    def set_sample_rate(self, sample_rate: int):

        self._sample_rate = sample_rate

        if self._device:

            self._device.sample_rate = sample_rate

        self.sample_rate_changed.emit(sample_rate)


    def set_gain(self, gain):

        self._gain = gain

        if not self._device:
            return

        self._device.gain = gain

        self.gain_changed.emit(gain)


    def set_ppm(self, ppm: int):

        self._ppm = ppm

        if self._device:

            self._device.freq_correction = ppm

    def read_samples(self, count=262144):

        if self._device is None:
            return None

        return self._device.read_samples(count)