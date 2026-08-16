import numpy as np
from gnuradio import gr, blocks, filter, fft
from gnuradio.fft import window
import osmosdr


class Receiver(gr.top_block):
    def __init__(self, frequency=437500000, sample_rate=2000000, gain=30, fft_size=256):
        super().__init__("RTL-SDR Receiver Flowgraph")

        self.fft_size = fft_size

        # 1. منبع دریافت RTL-SDR
        self.rtlsdr_source = osmosdr.source(args="rtl=0")
        self.rtlsdr_source.set_sample_rate(sample_rate)
        self.rtlsdr_source.set_center_freq(frequency, 0)
        self.rtlsdr_source.set_gain_mode(False, 0)
        self.rtlsdr_source.set_gain(gain, 0)

        # 2. محاسبه FFT برای نمودار طیف و آبشاری
        self.stream_to_vector = blocks.stream_to_vector(gr.sizeof_gr_complex, self.fft_size)
        self.fft_block = fft.fft_vcc(self.fft_size, True, window.blackmanharris(self.fft_size), True)
        self.complex_to_mag_squared = blocks.complex_to_mag_squared(self.fft_size)

        # 3. سینک خروجی داده‌های FFT
        self.vector_sink = blocks.probe_signal_vf(self.fft_size)

        # اتصال بلوک‌ها
        self.connect(self.rtlsdr_source, self.stream_to_vector)
        self.connect(self.stream_to_vector, self.fft_block)
        self.connect(self.fft_block, self.complex_to_mag_squared)
        self.connect(self.complex_to_mag_squared, self.vector_sink)

    def set_frequency(self, freq):
        self.rtlsdr_source.set_center_freq(freq, 0)

    def set_sample_rate(self, rate):
        self.rtlsdr_source.set_sample_rate(rate)

    def set_gain(self, gain):
        self.rtlsdr_source.set_gain(gain, 0)

    def get_fft_data(self):
        # دریافت داده‌های FFT و تبدیل به dBFS
        data = np.array(self.vector_sink.level())
        data = 10 * np.log10(data + 1e-12)
        return np.fft.fftshift(data)