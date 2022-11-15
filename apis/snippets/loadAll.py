import os.path
import sys
sys.path.insert(0, '../')

from apis.snippets.loadSingle import runSingle
import asyncio
from util.defaultOSC import SimpleClient
from PyQt6.QtWidgets import (
    QMessageBox,
    QPushButton,
)

class LoadAllButton(QPushButton):
    def __init__(self, widgets, server, filenames, personal):
        super().__init__("Load All")
        self.widgets = widgets
        self.server = server
        self.filenames = filenames
        self.personal = personal
        self.pressed.connect(self.clicked)
    
    def clicked(self):
        asyncio.run(main(
            SimpleClient(self.widgets["ip"]["FOH"].text()),
            SimpleClient(self.widgets["ip"]["IEM"].text()),
            self.server,
            self.filenames,
            self.personal
        ))
        
        dlg = QMessageBox(self)
        dlg.setWindowTitle("Load All")
        dlg.setText("All Settings Loaded")
        dlg.exec()
        
async def main(fohClient, iemClient, server, filenames, personal):
    for chName in filenames:
        if (filenames[chName].currentText() != ""):
            if (os.path.exists("data/" + filenames[chName].currentText())):
                await runSingle(fohClient, iemClient, server, filenames[chName].currentText())
                personal[chName].setCurrentText(filenames[chName].currentText().split(".")[0].split("_")[2])
            else:
                print("Invalid filename for " + chName)