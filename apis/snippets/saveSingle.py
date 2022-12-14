from datetime import date
import os
from PyQt6.QtWidgets import (
    QMessageBox,
    QPushButton,
)
import traceback
from util.constants import ODD_BUSES, ALL_CHANNELS, SETTINGS
from util.customWidgets import ProgressDialog


class SaveButton(QPushButton):
    def __init__(self, osc, chName, personName, config):
        super().__init__("Save")
        self.osc = osc
        self.chName = chName
        self.personName = personName
        self.config = config
        self.pressed.connect(self.clicked)
        self.setFixedWidth(80)
    
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
            # Produce Header Line
            tags = {}
            headersLine = []
            if "channels" in config:
                for idx, channel in enumerate(config["channels"]):
                    key = "<ch" + str(idx) + ">"
                    value = "/ch/" + channel
                    tags[value] = key
                    headersLine.append(key + "=" + value)
            if "iem_bus" in config:
                key = "<iem_bus>"
                value = "mix/" + config["iem_bus"]
                tags[value] = key
                headersLine.append(key + "=" + value)
            file.write(" ".join(headersLine))

            if "channels" in config:
                saveChannels(osc, file, tags, config["channels"], dlg)

            if "iem_bus" in config:
                saveIEMBus(osc, file, tags, config["iem_bus"], dlg)
        
        print("Created " + filename)
    except Exception as ex:
        os.remove("data/" + filename)
        raise ex

def saveChannels(osc, file, tags, channels, dlg = None):
    settings = {}
    for channel in channels:
        for category in SETTINGS:
            for param in SETTINGS[category]:
                settings["/ch/" + channel + param] = None

    saveSettingsToFile(osc, file, tags, "foh", settings, dlg)    

def saveIEMBus(osc, file, tags, bus, dlg = None):
    settings = {}
    for channel in ALL_CHANNELS:
        prefix = channel + "/mix/" + bus

        settings[prefix + "/on"] = None
        settings[prefix + "/level"] = None

        if bus in ODD_BUSES:
            settings[prefix + "/pan"] = None
    
    saveSettingsToFile(osc, file, tags, "iem", settings, dlg)

def saveSettingsToFile(osc, file, tags, prefix, settings, dlg = None):
    lines = getSettings(osc, prefix, settings, dlg)

    for line in lines:
        for value in tags:
            line = line.replace(value, tags[value])

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

        lines.append(prefix + " " + setting + " " + type + " " + str(value))
    
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