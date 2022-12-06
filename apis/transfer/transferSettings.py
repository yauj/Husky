import sys
import traceback
sys.path.insert(0, '../')

from util.constants import COPY_CHANNELS, LINK_CHANNELS, SETTINGS
from PyQt6.QtWidgets import (
    QMessageBox,
    QPushButton,
)

class TransferButton(QPushButton):
    def __init__(self, widgets, osc):
        super().__init__("Yes!")
        self.widgets = widgets
        self.osc = osc
        self.pressed.connect(self.clicked)
    
    def clicked(self):
        try:
            main(
                self.osc
            )
            
            dlg = QMessageBox(self)
            dlg.setWindowTitle("FOH->IEM")
            dlg.setText("Settings Transfered")
            dlg.exec()
        except Exception as ex:
            print(traceback.format_exc())
            dlg = QMessageBox(self)
            dlg.setWindowTitle("FOH->IEM")
            dlg.setText("Error: " + str(ex))
            dlg.exec()

        self.setDown(False)

def main(osc):
    settings = {}

    # Copy Channel Links
    for chlink in LINK_CHANNELS:
        settings["/config/chlink/" + chlink] = None

    # COPY_CHANNELS excludes FOH talkback channel
    for channel in COPY_CHANNELS:
        for category in SETTINGS:
            for param in SETTINGS[category]:
                settings[channel + param] = None
    
    values = osc["fohClient"].bulk_send_messages(settings)
    osc["iemClient"].bulk_send_messages(values)
    
    print("Settings Transferred")