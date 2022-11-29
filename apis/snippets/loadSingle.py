import os.path
import sys

import mido
sys.path.insert(0, '../')

import asyncio
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
                asyncio.run(main(
                    self.osc,
                    self.filename.currentText()
                ))

                self.person.setCurrentText(self.filename.currentText().split(".")[0].split("_")[2])
                
                dlg = QMessageBox(self)
                dlg.setWindowTitle("Load")
                dlg.setText("Loaded " + self.filename.currentText() + " for " + self.chName)
                dlg.exec()
            except Exception as ex:
                print(ex)
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
        
async def main(osc, filename):
    await runSingle(osc, filename, True)

async def runSingle(osc, filename, iemCopy):
    with open("data/" + filename) as scnFile:
        scnFile.readline() # Skip Header Line
        while (line := scnFile.readline().strip()):
            await fireLine(osc, line, iemCopy)

    print("Loaded " + filename + "\n")

async def fireLine(osc, line, iemCopy):
    components = line.split()

    if components[0] == "midi":
        channel = int(components[2]) - 1
        control = int(components[3])
        value = int(components[4])
        if (components[1] == "audio"):
            osc["audioMidi"].send(mido.Message("control_change", channel = channel, control = control, value = value))
        elif (components[1] == "video"):
            osc["videoMidi"].send(mido.Message("control_change", channel = channel, control = control, value = value))
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

        if (components[0] == "foh"):
            await osc["fohClient"].send_message(components[1], arg)
            if iemCopy: # Whether not to send setting to IEM mixer as well
                await osc["iemClient"].send_message(components[1], arg)
        elif (components[0] == "iem"):
            await osc["iemClient"].send_message(components[1], arg)