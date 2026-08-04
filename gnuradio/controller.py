class GNUController:

    def __init__(self):
        self.running = False

    def start(self):
        self.running = True
        print("Receiver Started")

    def stop(self):
        self.running = False
        print("Receiver Stopped")

    def set_frequency(self, freq):
        print("Frequency:", freq)

    def set_gain(self, gain):
        print("Gain:", gain)

    def set_sample_rate(self, rate):
        print("Sample Rate:", rate)