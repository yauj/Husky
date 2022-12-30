from datetime import date
import os
from PyQt6.QtWidgets import (
    QMessageBox,
    QPushButton,
)
import traceback
from util.constants import SETTINGS, SETTINGS_MAIN, formatBus, getAllChannels, getConfig, getMainPrefix, getOddBuses
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
            if self.chName == "Mains":
                dlg.setText("No Venue specified.")
            else: 
                dlg.setText("No person name specified for " + self.chName)
            dlg.exec()
        
        self.setDown(False)
        
    def main(self, dlg):
        try:
            dlg.initBar.emit(saveSingleNumSettings(self.config, self.osc, self.chName))
            runSingle(self.osc, self.chName, self.personName.currentText(), self.config, dlg)
            dlg.complete.emit()
        except Exception as ex:
            print(traceback.format_exc())
            dlg.raiseException.emit(ex)

def runSingle(osc, chName, personName, config, dlg = None):
    today = date.today().strftime("%Y%m%d")
    filename = today + "_" + chName + "_" + personName + ".osc"
    try:
        with open("data/" + filename, "w") as file:
            if chName == "Mains":
                saveMains(osc, file, dlg)
            else:
                # Produce Header Line
                file.write("v1.0")
                tags = {}

                fohConfig = getConfig(config["personal"][chName], osc["fohClient"].mixerType)
                iemConfig = getConfig(config["personal"][chName], osc["iemClient"].mixerType)

                if fohConfig is not None and "channels" in fohConfig:
                    for idx, channel in enumerate(fohConfig["channels"]):
                        key = "<ch" + str(idx) + ">"
                        value = "/ch/" + channel
                        tags[value] = key
                        file.write(" " + key + "=" + value)

                if iemConfig is not None and "iem_bus" in iemConfig:
                    key = "<iem_bus>"
                    value = "mix/" + formatBus(iemConfig["iem_bus"], osc["iemClient"].mixerType)
                    tags[value] = key
                    file.write(" " + key + "=" + value)

                if fohConfig is not None and "channels" in fohConfig:
                    saveChannels(osc, file, tags, fohConfig["channels"], dlg)

                if iemConfig is not None and "iem_bus" in iemConfig:
                    saveIEMBus(osc, file, tags, iemConfig["iem_bus"], dlg)
        
        print("Created " + filename)
    except Exception as ex:
        os.remove("data/" + filename)
        raise ex

def saveMains(osc, file, dlg = None):
    # Produce Header Line
    file.write("v1.0")
    tags = {}
    key = "<main>"
    value = getMainPrefix(osc["fohClient"].mixerType)
    tags[value] = key
    file.write(" " + key + "=" + value)

    settings = {}
    for category in SETTINGS_MAIN:
        for param in SETTINGS_MAIN[category]:
            settings[value + param] = None
    
    saveSettingsToFile(osc, file, tags, "foh", settings, dlg)    

def saveChannels(osc, file, tags, channels, dlg = None):
    settings = {}
    for channel in channels:
        for category in SETTINGS:
            for param in SETTINGS[category]:
                settings["/ch/" + channel + param] = None

    saveSettingsToFile(osc, file, tags, "foh", settings, dlg)

def saveIEMBus(osc, file, tags, bus, dlg = None):
    settings = {}
    for channel in getAllChannels(osc["iemClient"].mixerType):
        prefix = channel + "/mix/" + formatBus(bus, osc["iemClient"].mixerType)

        settings[prefix + "/on"] = None
        settings[prefix + "/level"] = None

        if bus in getOddBuses(osc["iemClient"].mixerType):
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

def saveSingleNumSettings(config, osc, chName):
    num = 0
    if chName == "Mains":
        for category in SETTINGS_MAIN:
            num = num + len(SETTINGS_MAIN[category])
    else:
        fohConfig = getConfig(config["personal"][chName], osc["fohClient"].mixerType)
        iemConfig = getConfig(config["personal"][chName], osc["iemClient"].mixerType)

        if fohConfig is not None and "channels" in fohConfig:
            channelNum = 0
            for category in SETTINGS:
                channelNum = channelNum + len(SETTINGS[category])
            
            channelNum = channelNum * len(fohConfig["channels"])
            num = num + channelNum

        if iemConfig is not None and "iem_bus" in iemConfig:
            iemNum = len(getAllChannels(osc["iemClient"].mixerType))
            if formatBus(iemConfig["iem_bus"], osc["iemClient"].mixerType) in getOddBuses(osc["iemClient"].mixerType):
                iemNum = iemNum * 3
            else:
                iemNum = iemNum * 2
            
            num = num + iemNum

    return num