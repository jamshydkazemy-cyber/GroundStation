from gnuradio.receiver import Receiver


class GNUController:

    def __init__(self):

        self.tb = None

    def start(self):

        if self.tb is None:

            self.tb = Receiver()

            self.tb.start()

    def stop(self):

        if self.tb:

            self.tb.stop()

            self.tb.wait()

            self.tb = None