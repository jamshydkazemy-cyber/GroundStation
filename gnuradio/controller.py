class GNUController:

    def __init__(self):
        self.tb = None
        self.frequency = 437500000.0
        self.sample_rate = 2000000
        self.gain = 30

    def set_frequency(self, freq: float):
        self.frequency = freq
        if self.tb:
            self.tb.set_frequency(freq)

    def set_sample_rate(self, rate: int):
        self.sample_rate = rate
        if self.tb:
            self.tb.set_sample_rate(rate)

    def set_gain(self, gain: int):
        self.gain = gain
        if self.tb:
            self.tb.set_gain(gain)

    def start(self):
        if self.tb is None:
            try:
                from gnuradio.receiver import Receiver
                self.tb = Receiver(
                    frequency=self.frequency,
                    sample_rate=self.sample_rate,
                    gain=self.gain
                )
                self.tb.start()
            except Exception as e:
                print(f"GNU Radio Error: {e}. Running in standalone test mode.")

    def stop(self):
        if self.tb:
            self.tb.stop()
            self.tb.wait()
            self.tb = None

    def get_fft_data(self):
        if self.tb and hasattr(self.tb, 'get_fft_data'):
            return self.tb.get_fft_data()
        return None