import sys
sys.path.insert(0, '../')

import asyncio
from util.constants import COPY_CHANNELS, LINK_CHANNELS
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
        asyncio.run(main(
            self.osc
        ))
        
        dlg = QMessageBox(self)
        dlg.setWindowTitle("FOH->IEM")
        dlg.setText("Settings Transfered")
        dlg.exec()

async def main(osc):
    # Copy Channel Links
    for chlink in LINK_CHANNELS:
        await transferSetting(osc, "/config/chlink/" + chlink)

    for channel in COPY_CHANNELS:
        # Copy Channel Labeling (except FOH talkback)
        for param in ["name", "icon", "color"]:
            await transferSetting(osc, channel + "/config/" + param) 

        # Copy Low Cut
        for param in ["hpon", "hpf"]:
            await transferSetting(osc, channel + "/preamp/" + param)

        # Copy EQ Settings
        for band in ["1", "2", "3", "4"]:
            for param in ["type", "f", "g", "q"]:
                await transferSetting(osc, channel + "/eq/" + band + "/" + param)

        # Copy Compression Setting
        for param in ["thr", "ratio", "knee", "mgain", "attack", "hold", "release", "mix"]:
            await transferSetting(osc, channel + "/dyn/" + param)
    
    print("Settings Transferred")

async def transferSetting(osc, command):
    await osc["fohClient"].send_message(command, None)
    osc["server"].handle_request()
    await osc["iemClient"].send_message(command, osc["server"].lastVal)

