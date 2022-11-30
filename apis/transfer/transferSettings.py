import sys
sys.path.insert(0, '../')

import asyncio
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
            asyncio.run(main(
                self.osc
            ))
            
            dlg = QMessageBox(self)
            dlg.setWindowTitle("FOH->IEM")
            dlg.setText("Settings Transfered")
            dlg.exec()
        except Exception as ex:
            print(ex)
            dlg = QMessageBox(self)
            dlg.setWindowTitle("FOH->IEM")
            dlg.setText("Error: " + str(ex))
            dlg.exec()

        self.setDown(False)

async def main(osc):
    # Copy Channel Links
    for chlink in LINK_CHANNELS:
        await transferSetting(osc, "/config/chlink/" + chlink)

    # COPY_CHANNELS excludes FOH talkback channel
    for channel in COPY_CHANNELS:
        for category in SETTINGS:
            for param in SETTINGS[category]:
                await transferSetting(osc, channel + param)
    
    print("Settings Transferred")

async def transferSetting(osc, command):
    await osc["fohClient"].send_message(command, None)
    osc["server"].handle_request()
    await osc["iemClient"].send_message(command, osc["server"].lastVal)

