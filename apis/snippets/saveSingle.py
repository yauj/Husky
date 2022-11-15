import sys
sys.path.insert(0, '../')

import asyncio
from datetime import date
from util.constants import ODD_BUSES, ALL_CHANNELS
from util.defaultOSC import SimpleClient
from PyQt6.QtWidgets import (
    QMessageBox,
    QPushButton,
)

class SaveButton(QPushButton):
    def __init__(self, widgets, server, chName, personName, config):
        super().__init__("Save")
        self.widgets = widgets
        self.server = server
        self.chName = chName
        self.personName = personName
        self.config = config
        self.pressed.connect(self.clicked)
    
    def clicked(self):
        if (self.personName.currentText() != ""):
            asyncio.run(main(
                SimpleClient(self.widgets["ip"]["FOH"].text()),
                SimpleClient(self.widgets["ip"]["IEM"].text()),
                self.server,
                self.chName + "_" + self.personName.currentText(),
                self.config
            ))
            
            dlg = QMessageBox(self)
            dlg.setWindowTitle("Save")
            dlg.setText("Settings Saved for " + self.chName)
            dlg.exec()
        else:
            dlg = QMessageBox(self)
            dlg.setWindowTitle("Save")
            dlg.setText("No person name specified for " + self.chName)
            dlg.exec()
        
async def main(fohClient, iemClient, server, label, config):
    await runSingle(fohClient, iemClient, server, label, config)

async def runSingle(fohClient, iemClient, server, label, config):
    fohClient._sock = server.socket
    iemClient._sock = server.socket

    await fohClient.send_message("/info", None)
    server.handle_request()

    await iemClient.send_message("/info", None)
    server.handle_request()

    today = date.today().strftime("%Y%m%d")
    filename = today + "_" + label + ".osc"
    with open("data/" + filename, "w") as scnFile:
        if "channels" in config:
            for channel in config["channels"]:
                # Channel Labeling
                for param in ["name", "icon", "color"]:
                    await saveSetting(scnFile, "foh", fohClient, server, "/ch/" + channel + "/config/" + param)

                # Low Cut
                for param in ["hpon", "hpf"]:
                    await saveSetting(scnFile, "foh", fohClient, server, "/ch/" + channel + "/preamp/" + param)
                
                # EQ Settings
                for band in ["1", "2", "3", "4"]:
                    for param in ["type", "f", "g", "q"]:
                        await saveSetting(scnFile, "foh", fohClient, server, "/ch/" + channel + "/eq/" + band + "/" + param)

                # Compression Setting
                for param in ["thr", "ratio", "knee", "mgain", "attack", "hold", "release", "mix"]:
                    await saveSetting(scnFile, "foh", fohClient, server, "/ch/" + channel + "/dyn/" + param)

        if "iem_bus" in config:
            for channel in ALL_CHANNELS:
                prefix = channel + "/mix/" + config["iem_bus"]

                await saveSetting(scnFile, "iem", iemClient, server, prefix + "/on")
                await saveSetting(scnFile, "iem", iemClient, server, prefix + "/level")

                if config["iem_bus"] in ODD_BUSES:
                    await saveSetting(scnFile, "iem", iemClient, server, prefix + "/pan")

    print("Created " + filename + "\n")

async def saveSetting(file, prefix, client, server, setting):
    await client.send_message(setting, None)
    server.handle_request()
    type = "str"
    if (isinstance(server.lastVal, int)):
        type = "int"
    elif (isinstance(server.lastVal, float)):
        type = "float"

    file.write("\n" + prefix + " " + setting + " " + str(server.lastVal) + " " + type)