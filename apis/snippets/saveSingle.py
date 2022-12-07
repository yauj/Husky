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
from util.customWidgets import ProgressDialog


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
            dlg = ProgressDialog("Settings for " + self.chName + " Sav", self.main)
            dlg.exec()
        else:
            dlg = QMessageBox(self)
            dlg.setWindowTitle("Save")
            dlg.setText("No person name specified for " + self.chName)
            dlg.exec()
        
        self.setDown(False)
        
    def main(self, dlg):
        try:
            dlg.initBar.emit(saveSingleNumSettings(self.config))
            label = self.chName + "_" + self.personName.currentText()
            runSingle(self.osc, label, self.config, dlg)
            dlg.complete.emit()
        except Exception as ex:
            print(traceback.format_exc())
            dlg.raiseException.emit(ex)

def runSingle(osc, label, config, dlg = None):
    today = date.today().strftime("%Y%m%d")
    filename = today + "_" + label + ".osc"
    try:
        with open("data/" + filename, "w") as file:
            if "channels" in config:
                saveChannels(osc, file, config["channels"], dlg)

            if "iem_bus" in config:
                saveIEMBus(osc, file, config["iem_bus"], dlg)
        
        print("Created " + filename)
    except Exception as ex:
        os.remove("data/" + filename)
        raise ex

def saveChannels(osc, file, channels, dlg = None):
    settings = {}
    for channel in channels:
        for category in SETTINGS:
            for param in SETTINGS[category]:
                settings["/ch/" + channel + param] = None

    saveSettingsToFile(osc, file, "foh", settings, dlg)    

def saveIEMBus(osc, file, bus, dlg = None):
    settings = {}
    for channel in ALL_CHANNELS:
        prefix = channel + "/mix/" + bus

        settings[prefix + "/on"] = None
        settings[prefix + "/level"] = None

        if bus in ODD_BUSES:
            settings[prefix + "/pan"] = None
    
    saveSettingsToFile(osc, file, "iem", settings, dlg)

def saveSettingsToFile(osc, file, prefix, settings, dlg = None):
    lines = getSettings(osc, prefix, settings, dlg)

    for line in lines:
        file.write("\n" + line)

def appendSettingsToTextbox(osc, textbox, prefix, settings):
    lines = getSettings(osc, prefix, settings)

    for line in lines:
        textbox.append(line)

def getSettings(osc, prefix, settings, dlg = None):
    values = osc[prefix + "Client"].bulk_send_messages(settings, dlg)
    
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

def saveSingleNumSettings(config):
    num = 0
    if "channels" in config:
        channelNum = 0
        for category in SETTINGS:
            channelNum = channelNum + len(SETTINGS[category])
        
        channelNum = channelNum * len(config["channels"])
        num = num + channelNum

    if "iem_bus" in config:
        iemNum = len(ALL_CHANNELS)
        if config["iem_bus"] in ODD_BUSES:
            iemNum = iemNum * 3
        else:
            iemNum = iemNum * 2
        
        num = num + iemNum

    return num