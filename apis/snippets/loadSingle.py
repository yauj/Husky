import os.path
import sys
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
            components = line.split()

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
            
    print("Loaded " + filename + "\n")