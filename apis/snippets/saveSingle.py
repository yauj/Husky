import os
import sys
import traceback
sys.path.insert(0, '../')

import asyncio
from datetime import date
from util.constants import ODD_BUSES, ALL_CHANNELS, SETTINGS
from PyQt6.QtWidgets import (
    QMessageBox,
    QPushButton,
)

class SaveButton(QPushButton):
    def __init__(self, widgets, osc, chName, personName, config):
        super().__init__("Save")
        self.widgets = widgets
        self.osc = osc
        self.chName = chName
        self.personName = personName
        self.config = config
        self.pressed.connect(self.clicked)
    
    def clicked(self):
        if (self.personName.currentText() != ""):
            try:
                asyncio.run(main(
                    self.osc,
                    self.chName + "_" + self.personName.currentText(),
                    self.config
                ))
                
                dlg = QMessageBox(self)
                dlg.setWindowTitle("Save")
                dlg.setText("Settings Saved for " + self.chName)
                dlg.exec()
            except Exception as ex:
                print(traceback.format_exc())
                dlg = QMessageBox(self)
                dlg.setWindowTitle("Save")
                dlg.setText("Error: " + str(ex))
                dlg.exec()
        else:
            dlg = QMessageBox(self)
            dlg.setWindowTitle("Save")
            dlg.setText("No person name specified for " + self.chName)
            dlg.exec()
        
        self.setDown(False)
        
async def main(osc, label, config):
    await runSingle(osc, label, config)

async def runSingle(osc, label, config):
    today = date.today().strftime("%Y%m%d")
    filename = today + "_" + label + ".osc"
    try:
        with open("data/" + filename, "w") as file:
            if "channels" in config:
                await saveChannels(osc, file, config["channels"])

            if "iem_bus" in config:
                await saveIEMBus(osc, file, config["iem_bus"])
        
        print("Created " + filename + "\n")
    except Exception as ex:
        os.remove("data/" + filename)
        raise ex

async def saveChannels(osc, file, channels):
    for channel in channels:
        for category in SETTINGS:
            for param in SETTINGS[category]:
                await saveSetting(file, "foh", osc["fohClient"], osc["server"], "/ch/" + channel + param)

async def saveIEMBus(osc, file, bus):
    for channel in ALL_CHANNELS:
        prefix = channel + "/mix/" + bus

        await saveSetting(file, "iem", osc["iemClient"], osc["server"], prefix + "/on")
        await saveSetting(file, "iem", osc["iemClient"], osc["server"], prefix + "/level")

        if bus in ODD_BUSES:
            await saveSetting(file, "iem", osc["iemClient"], osc["server"], prefix + "/pan")

async def saveSetting(file, prefix, client, server, setting):
    line = await getSetting(prefix, client, server, setting)
    file.write("\n" + line)

async def getSetting(prefix, client, server, setting):
    await client.send_message(setting, None)
    server.handle_request()
    type = "str"
    if (isinstance(server.lastVal, int)):
        type = "int"
    elif (isinstance(server.lastVal, float)):
        type = "float"

    return prefix + " " + setting + " " + str(server.lastVal) + " " + type