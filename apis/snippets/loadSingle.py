import logging
import subprocess
import mido
import os.path
from PyQt6.QtWidgets import (
    QMessageBox,
    QPushButton,
)
import traceback
from util.customWidgets import ProgressDialog

logger = logging.getLogger(__name__)

class LoadButton(QPushButton):
    def __init__(self, config, widgets, osc, chName, filename, person):
        super().__init__("Load")
        self.config = config
        self.widgets = widgets
        self.osc = osc
        self.chName = chName
        self.filename = filename
        self.person = person
        self.pressed.connect(self.clicked)
        self.setFixedWidth(80)

    def clicked(self):
        if (self.filename.currentText() != "" and os.path.exists("data/" + self.filename.currentText())):
            dlg = ProgressDialog("Settings for " + self.chName + " Load", self.main)
            dlg.exec()
        else:
            dlg = QMessageBox(self)
            dlg.setWindowTitle("Load")
            dlg.setText("Invalid Filename for " + self.chName)
            dlg.exec()
        
        self.setDown(False)
        
    def main(self, dlg):
        try:
            dlg.initBar.emit(loadSingleNumSettings(self.config, "data/" + self.filename.currentText(), self.chName != "Mains"))
            runSingle(self.config, self.widgets, self.osc, "data/" + self.filename.currentText(), self.chName != "Mains", self.chName, dlg)
            self.person.setCurrentText(self.filename.currentText().split(".")[0].split("_")[2])
            dlg.complete.emit()
        except Exception as ex:
            logger.error(traceback.format_exc())
            dlg.raiseException.emit(ex)

def runSingle(config, widgets, osc, filename, iemCopy = False, chName = None, dlg = None):
    lines = []
    with open(filename) as scnFile:
        # Process Headers
        tags = {}
        replaceTags = {} # Extra tags to replace
        removeTags = {} # Commands that are to be removed
        headerLine = scnFile.readline().strip()
        if headerLine != "":
            if chName != None:
                # Loading to chName
                if "channels" in config["personal"][chName]:
                    for idx, channel in enumerate(config["personal"][chName]["channels"]):
                        key = "<ch" + str(idx) + ">"
                        value = "/ch/" + channel
                        tags[key] = value
                if "iem_bus" in config["personal"][chName]:
                    if config["personal"][chName]["iem_bus"] != "st" and config["personal"][chName]["iem_bus"] != "mono":
                        key = "<iem_bus>"
                        value = "mix/" + config["personal"][chName]["iem_bus"]
                        tags[key] = value

                for pair in headerLine.split()[1:]:
                    keyVal = pair.split("=")
                    if (keyVal[0] not in tags):
                        removeTags[keyVal[0]] = keyVal[1]
                    elif (keyVal[1] != tags[keyVal[0]]):
                        replaceTags[tags[keyVal[0]]] = keyVal[1]
            else:
                # Default to what is given in the header tags
                for pair in headerLine.split()[1:]:
                    keyVal = pair.split("=")
                    tags[keyVal[0]] = keyVal[1]

        # Process remaining lines
        while (line := scnFile.readline().strip()):
            keepLine = True
            for key in removeTags:
                if key in line:
                    line = line.replace(key, removeTags[key])
                    keepLine = False
            for key in replaceTags:
                line = line.replace(key, replaceTags[key])
            for key in tags:
                if key in line:
                    line = line.replace(key, tags[key])
                    keepLine = True

            if keepLine:
                lines.append(line)

    fireLines(config, widgets, osc, lines, iemCopy, dlg)

    logger.info("Loaded " + filename)

def fireLines(config, widgets, osc, lines, iemCopy = False, dlg = None):
    settings = {"foh": {}, "iem": {}, "atem": {}}
    fadeSettings = {"foh": {}, "iem": {}, "atem": {}}
    for mixerName in config["osc"]: # Make sure that any additional mixers will be added
        settings[mixerName] = {}
        fadeSettings[mixerName] = {}

    for line in lines:
        components = line.split()

        if components[0] == "lucky":
            if "AutoMixLucky" in widgets["windows"]: # Do nothing if window not open
                if components[1] in widgets["windows"]["AutoMixLucky"].assignments:
                    widgets["windows"]["AutoMixLucky"].assignments[components[1]].setCurrentText(components[2])
                    if len(components) >= 4: # Then we want to load weight as well
                        channelIdx = int(components[1].replace("/ch/", "")) - 1
                        widgets["windows"]["AutoMixLucky"].weights[channelIdx].setValue(float(components[3]))
        elif components[0] == "open":
            subprocess.Popen(line, shell = True) # Just open file in background (Only Mac Compatiable)
        elif components[0] == "midi":
            channel = int(components[2]) - 1
            control = int(components[3])
            value = int(components[4])
            if components[1] in config["midi"]:
                if config["midi"][components[1]]["type"] == "cc":
                    osc[components[1] + "Midi"].send(mido.Message("control_change", channel = channel, control = control, value = value))
                elif config["midi"][components[1]]["type"] == "note":
                    if value == 0:
                        osc[components[1] + "Midi"].send(mido.Message("note_off", channel = channel, note = control))
                    else:
                        osc[components[1] + "Midi"].send(mido.Message("note_on", channel = channel, note = control))
        elif components[0] in settings:
            arg = " ".join(components[3:])
            fadeTime = None
            if (components[2] == "int"):
                arg = int(components[3])
            elif (components[2] == "float"):
                arg = float(components[3])
                if len(components) >= 5:
                    fadeTime = float(components[4])
            
            if fadeTime is not None:
                fadeSettings[components[0]][components[1]] = {"endVal": arg, "fadeTime": fadeTime}
            else:
                settings[components[0]][components[1]] = arg

            if (components[0] == "foh" and iemCopy):
                if fadeTime is not None:
                    fadeSettings["iem"][components[1]] = {"endVal": arg, "fadeTime": fadeTime}
                else:
                    settings["iem"][components[1]] = arg
    
    for mixerName in settings:
        if len(settings[mixerName]) > 0 or len(fadeSettings[mixerName]) > 0:
            osc[mixerName + "Client"].bulk_send_messages(settings[mixerName], dlg, fadeSettings[mixerName])

def loadSingleNumSettings(config, filename, iemCopy = False):
    num = 0
    if (os.path.exists(filename)):
        with open(filename) as file:
            file.readline() # Skip Header Line
            while (line := file.readline().strip()):
                components = line.split()

                if components[0] in ["foh", "iem", "atem"] or components[0] in config["osc"]:
                    num = num + 1
                
                if components[0] == "foh" and iemCopy:
                    num = num + 1

    return num
