import sys
sys.path.insert(0, '../')

from apis.snippets.saveSingle import runSingle
import asyncio
from util.defaultOSC import SimpleClient
from PyQt6.QtWidgets import (
    QMessageBox,
    QPushButton,
)

class SaveAllButton(QPushButton):
    def __init__(self, widgets, server, personNames, config):
        super().__init__("Save All")
        self.widgets = widgets
        self.server = server
        self.personNames = personNames
        self.config = config
        self.pressed.connect(self.clicked)
    
    def clicked(self):
        asyncio.run(main(
            SimpleClient(self.widgets["ip"]["FOH"].text()),
            SimpleClient(self.widgets["ip"]["IEM"].text()),
            self.server,
            self.personNames,
            self.config
        ))
        
        dlg = QMessageBox(self)
        dlg.setWindowTitle("Save All")
        dlg.setText("All Settings Saved")
        dlg.exec()
        
async def main(fohClient, iemClient, server, personNames, config):
    for chName in personNames:
        if (personNames[chName].currentText() != ""):
            await runSingle(fohClient, iemClient, server, chName + "_" + personNames[chName].currentText(), config[chName])
