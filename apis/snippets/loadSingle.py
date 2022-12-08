import os.path
import sys
import traceback
sys.path.insert(0, '../')

import mido
from PyQt6.QtWidgets import (
    QMessageBox,
    QPushButton,
)
from util.customWidgets import ProgressDialog

class LoadButton(QPushButton):
    def __init__(self, osc, chName, filename, person):
        super().__init__("Load")
        self.osc = osc
        self.chName = chName
        self.filename = filename
        self.person = person
        self.pressed.connect(self.clicked)

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
            dlg.initBar.emit(loadSingleNumSettings(self.filename.currentText(), True))
            runSingle(self.osc, self.filename.currentText(), True, dlg)
            self.person.setCurrentText(self.filename.currentText().split(".")[0].split("_")[2])
            dlg.complete.emit()
        except Exception as ex:
            print(traceback.format_exc())
            dlg.raiseException.emit(ex)

def runSingle(osc, filename, iemCopy, dlg = None):
    lines = []
    with open("data/" + filename) as scnFile:
        scnFile.readline() # Skip Header Line
        while (line := scnFile.readline().strip()):
            lines.append(line)
        
    fireLines(osc, lines, iemCopy, dlg)

    print("Loaded " + filename)

def fireLines(osc, lines, iemCopy, dlg = None):
    fohSettings = {}
    iemSettings = {}
    for line in lines:
        components = line.split()

        if components[0] == "midi":
            channel = int(components[2]) - 1
            control = int(components[3])
            value = int(components[4])
            if (components[1] == "audio"):
                osc["audioMidi"].send(mido.Message("control_change", channel = channel, control = control, value = value))
            elif (components[1] == "video"):
                if value == 0:
                    osc["videoMidi"].send(mido.Message("note_off", channel = channel, note = control))
                else:
                    osc["videoMidi"].send(mido.Message("note_on", channel = channel, note = control))
            elif (components[1] == "light"):
                if value == 0:
                    osc["lightMidi"].send(mido.Message("note_off", channel = channel, note = control))
                else:
                    osc["lightMidi"].send(mido.Message("note_on", channel = channel, note = control))
        else:
            arg = " ".join(components[3:])
            if (components[2] == "int"):
                arg = int(arg)
            elif (components[2] == "float"):
                arg = float(arg)

            if (components[0] == "foh"):
                fohSettings[components[1]] = arg
                if iemCopy: # Whether not to send setting to IEM mixer as well
                    iemSettings[components[1]] = arg
            elif (components[0] == "iem"):
                iemSettings[components[1]] = arg

    osc["fohClient"].bulk_send_messages(fohSettings, dlg)
    osc["iemClient"].bulk_send_messages(iemSettings, dlg)

def loadSingleNumSettings(filename, iemCopy):
    num = 0
    if (os.path.exists("data/" + filename)):
        with open("data/" + filename) as file:
            file.readline() # Skip Header Line
            while (line := file.readline().strip()):
                components = line.split()

                if (components[0] == "foh"):
                    if iemCopy:
                        num = num + 2
                    else:
                        num = num + 1
                elif (components[0] == "iem"):
                    num = num + 1
    return num
