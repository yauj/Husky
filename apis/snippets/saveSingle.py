import os
import sys
import traceback
sys.path.insert(0, '../')

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
                main(
                    self.osc,
                    self.chName + "_" + self.personName.currentText(),
                    self.config
                )
                
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
        
def main(osc, label, config):
    runSingle(osc, label, config)

def runSingle(osc, label, config):
    today = date.today().strftime("%Y%m%d")
    filename = today + "_" + label + ".osc"
    try:
        with open("data/" + filename, "w") as file:
            if "channels" in config:
                saveChannels(osc, file, config["channels"])

            if "iem_bus" in config:
                saveIEMBus(osc, file, config["iem_bus"])
        
        print("Created " + filename + "\n")
    except Exception as ex:
        os.remove("data/" + filename)
        raise ex

def saveChannels(osc, file, channels):
    settings = {}
    for channel in channels:
        for category in SETTINGS:
            for param in SETTINGS[category]:
                settings["/ch/" + channel + param] = None

    saveSettingsToFile(osc, file, "foh", settings)    

def saveIEMBus(osc, file, bus):
    settings = {}
    for channel in ALL_CHANNELS:
        prefix = channel + "/mix/" + bus

        settings[prefix + "/on"] = None
        settings[prefix + "/level"] = None

        if bus in ODD_BUSES:
            settings[prefix + "/pan"] = None
    
    saveSettingsToFile(osc, file, "iem", settings)

def saveSettingsToFile(osc, file, prefix, settings):
    lines = getSettings(osc, prefix, settings)

    for line in lines:
        file.write("\n" + line)

def appendSettingsToTextbox(osc, textbox, prefix, settings):
    lines = getSettings(osc, prefix, settings)

    for line in lines:
        textbox.append(line)

def getSettings(osc, prefix, settings):
    values = osc[prefix + "Client"].bulk_send_messages(settings)
    
    lines = []
    for setting in values:
        value = values[setting]
        type = "str"
        if (isinstance(value, int)):
            type = "int"
        elif (isinstance(value, float)):
            type = "float"

        lines.append(prefix + " " + setting + " " + str(value) + " " + type)
    
    lines.sort()
    return lines