import sys
import traceback
sys.path.insert(0, '../')

from util.constants import COPY_CHANNELS, LINK_CHANNELS, SETTINGS
from util.customWidgets import ProgressDialog
from PyQt6.QtWidgets import (
    QPushButton,
)

class TransferButton(QPushButton):
    def __init__(self, widgets, osc):
        super().__init__("Yes!")
        self.widgets = widgets
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
            for chlink in LINK_CHANNELS:
                settings["/config/chlink/" + chlink] = None

            # COPY_CHANNELS excludes FOH talkback channel
            for channel in COPY_CHANNELS:
                for category in SETTINGS:
                    for param in SETTINGS[category]:
                        settings[channel + param] = None

            dlg.initBar.emit(len(settings) * 2)
            
            values = self.osc["fohClient"].bulk_send_messages(settings, dlg)
            self.osc["iemClient"].bulk_send_messages(values, dlg)
            
            print("Settings Transferred")
            dlg.complete.emit()
        except Exception as ex:
            print(traceback.format_exc())
            dlg.raiseException.emit(ex)