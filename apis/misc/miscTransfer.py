from PyQt6.QtWidgets import (
    QPushButton,
)
import traceback
from util.constants import SETTINGS, getAllChannels, getAuxChannels, getLinkChannels
from util.customWidgets import ProgressDialog

class TransferButton(QPushButton):
    def __init__(self, config, osc):
        super().__init__("Transfer Settings from FOH to IEM Mixer")
        self.config = config
        self.osc = osc
        self.pressed.connect(self.clicked)
    
    def clicked(self):
        dlg = ProgressDialog("Settings Transfer", self.main)
        dlg.exec()

        self.setDown(False)

    def main(self, dlg):
        try:
            settings = {}

            # Copy Channel Links
            for chlink in getLinkChannels(self.osc["fohClient"].mixerType):
                settings["/config/chlink/" + chlink] = None

            # Exclude AUX and talkback channels
            channels = set(getAllChannels(self.osc["fohClient"].mixerType)) - set(getAuxChannels(self.osc["fohClient"].mixerType))
            if "talkbackChannel" in self.config:
                channels = channels - set([self.config["talkbackChannel"]])
            for channel in channels:
                for category in SETTINGS:
                    for param in SETTINGS[category]:
                        settings[channel + param] = None

            settings[channel + "/config/name"] = None

            dlg.initBar.emit(len(settings) * 2)
            
            values = self.osc["fohClient"].bulk_send_messages(settings, dlg)
            self.osc["iemClient"].bulk_send_messages(values, dlg)
            
            print("Settings Transferred")
            dlg.complete.emit()
        except Exception as ex:
            print(traceback.format_exc())
            dlg.raiseException.emit(ex)