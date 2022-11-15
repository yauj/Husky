import os.path
import sys
sys.path.insert(0, '../')

import asyncio
from util.defaultOSC import SimpleClient
from PyQt6.QtWidgets import (
    QMessageBox,
    QPushButton,
)

class LoadButton(QPushButton):
    def __init__(self, widgets, server, chName, filename, person):
        super().__init__("Load")
        self.widgets = widgets
        self.server = server
        self.chName = chName
        self.filename = filename
        self.person = person
        self.pressed.connect(self.clicked)

    def clicked(self):
        if (self.filename.currentText() != "" and os.path.exists("data/" + self.filename.currentText())):
            asyncio.run(main(
                SimpleClient(self.widgets["ip"]["FOH"].text()),
                SimpleClient(self.widgets["ip"]["IEM"].text()),
                self.server,
                self.filename.currentText()
            ))

            self.person.setCurrentText(self.filename.currentText().split(".")[0].split("_")[2])
            
            dlg = QMessageBox(self)
            dlg.setWindowTitle("Load")
            dlg.setText("Loaded " + self.filename.currentText() + " for " + self.chName)
            dlg.exec()
        else:
            dlg = QMessageBox(self)
            dlg.setWindowTitle("Load")
            dlg.setText("Invalid Filename for " + self.chName)
            dlg.exec()
        
async def main(fohClient, iemClient, server, filename):
    await runSingle(fohClient, iemClient, server, filename, True)

async def runSingle(fohClient, iemClient, server, filename, iemDynamics):
    fohClient._sock = server.socket
    iemClient._sock = server.socket

    await fohClient.send_message("/info", None)
    server.handle_request()

    await iemClient.send_message("/info", None)
    server.handle_request()

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
                await fohClient.send_message(components[1], arg)
                if iemDynamics: # Whether not to send Dynamics to IEM mixer as well
                    await iemClient.send_message(components[1], arg)
            elif (components[0] == "iem"):
                await iemClient.send_message(components[1], arg)
            
    print("Loaded " + filename + "\n")