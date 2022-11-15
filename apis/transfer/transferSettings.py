import sys
sys.path.insert(0, '../')

import asyncio
from util.constants import COPY_CHANNELS, LINK_CHANNELS
from util.defaultOSC import SimpleClient
from PyQt6.QtWidgets import (
    QMessageBox,
    QPushButton,
)

class TransferButton(QPushButton):
    def __init__(self, widgets, server):
        super().__init__("Yes!")
        self.widgets = widgets
        self.server = server
        self.pressed.connect(self.clicked)
    
    def clicked(self):
        asyncio.run(main(
            SimpleClient(self.widgets["ip"]["FOH"].text()),
            SimpleClient(self.widgets["ip"]["IEM"].text()),
            self.server
        ))
        
        dlg = QMessageBox(self)
        dlg.setWindowTitle("FOH->IEM")
        dlg.setText("Settings Transfered")
        dlg.exec()

async def main(fohClient, iemClient, server):
    fohClient._sock = server.socket
    iemClient._sock = server.socket

    await fohClient.send_message("/info", None)
    server.handle_request()

    await iemClient.send_message("/info", None)
    server.handle_request()
    # Copy Channel Links
    for chlink in LINK_CHANNELS:
        await transferSetting(fohClient, iemClient, server, "/config/chlink/" + chlink)

    for channel in COPY_CHANNELS:
        # Copy Channel Labeling (except FOH talkback)
        for param in ["name", "icon", "color"]:
            await transferSetting(fohClient, iemClient, server, channel + "/config/" + param) 

        # Copy Low Cut
        for param in ["hpon", "hpf"]:
            await transferSetting(fohClient, iemClient, server, channel + "/preamp/" + param)

        # Copy EQ Settings
        for band in ["1", "2", "3", "4"]:
            for param in ["type", "f", "g", "q"]:
                await transferSetting(fohClient, iemClient, server, channel + "/eq/" + band + "/" + param)

        # Copy Compression Setting
        for param in ["thr", "ratio", "knee", "mgain", "attack", "hold", "release", "mix"]:
            await transferSetting(fohClient, iemClient, server, channel + "/dyn/" + param)
    
    print("Settings Transferred")

async def transferSetting(fohClient, iemClient, server, command):
    await fohClient.send_message(command, None)
    server.handle_request()
    await iemClient.send_message(command, server.lastVal)

