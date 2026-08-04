from PySide6.QtWidgets import QStackedWidget

from gui.pages.receiver_page import ReceiverPage
from gui.pages.transmitter_page import TransmitterPage
from gui.pages.spectrum_page import SpectrumPage
from gui.pages.waterfall_page import WaterfallPage
from gui.pages.telemetry_page import TelemetryPage
from gui.pages.settings_page import SettingsPage


class PageManager(QStackedWidget):

    def __init__(self):
        super().__init__()

        self.receiver = ReceiverPage()
        self.transmitter = TransmitterPage()
        self.spectrum = SpectrumPage()
        self.waterfall = WaterfallPage()
        self.telemetry = TelemetryPage()
        self.settings = SettingsPage()

        self.addWidget(self.receiver)
        self.addWidget(self.transmitter)
        self.addWidget(self.spectrum)
        self.addWidget(self.waterfall)
        self.addWidget(self.telemetry)
        self.addWidget(self.settings)