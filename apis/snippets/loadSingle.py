import os.path
import sys
import traceback
sys.path.insert(0, '../')

import mido
from PyQt6.QtWidgets import (
    QMessageBox,
    QPushButton,
)

class LoadButton(QPushButton):
    def __init__(self, widgets, osc, chName, filename, person):
        super().__init__("Load")
        self.widgets = widgets
        self.osc = osc
        self.chName = chName
        self.filename = filename
        self.person = person
        self.pressed.connect(self.clicked)

    def clicked(self):
        if (self.filename.currentText() != "" and os.path.exists("data/" + self.filename.currentText())):
            try:
                main(
                    self.osc,
                    self.filename.currentText()
                )

                self.person.setCurrentText(self.filename.currentText().split(".")[0].split("_")[2])
                
                dlg = QMessageBox(self)
                dlg.setWindowTitle("Load")
                dlg.setText("Loaded " + self.filename.currentText() + " for " + self.chName)
                dlg.exec()
            except Exception as ex:
                print(traceback.format_exc())
                dlg = QMessageBox(self)
                dlg.setWindowTitle("Load")
                dlg.setText("Error: " + str(ex))
                dlg.exec() 
        else:
            dlg = QMessageBox(self)
            dlg.setWindowTitle("Load")
            dlg.setText("Invalid Filename for " + self.chName)
            dlg.exec()
        
        self.setDown(False)
        
def main(osc, filename):
    runSingle(osc, filename, True)

def runSingle(osc, filename, iemCopy):
    with open("data/" + filename) as scnFile:
        scnFile.readline() # Skip Header Line
        while (line := scnFile.readline().strip()):
            fireLine(osc, line, iemCopy)

    print("Loaded " + filename + "\n")

def fireLine(osc, line, iemCopy):
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
        arg = components[2]
        if (components[3] == "int"):
            arg = int(arg)
        elif (components[3] == "float"):
            arg = float(arg)
        elif (components[3] == "delta"):
            delta = float(arg)
            osc["fohClient"].send_message(components[1], None)
            osc["server"].handle_request()
            curVal = osc["server"].lastVal
            arg = curVal + delta

        if (components[0] == "foh"):
            osc["fohClient"].send_message(components[1], arg)
            if iemCopy: # Whether not to send setting to IEM mixer as well
                osc["iemClient"].send_message(components[1], arg)
        elif (components[0] == "iem"):
            osc["iemClient"].send_message(components[1], arg)