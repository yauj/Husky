import os.path
import sys
sys.path.insert(0, '../')

from apis.snippets.loadSingle import runSingle
import asyncio
from PyQt6.QtWidgets import (
    QMessageBox,
    QPushButton,
)

class LoadAllButton(QPushButton):
    def __init__(self, widgets, osc, filenames, personal):
        super().__init__("Load All")
        self.widgets = widgets
        self.osc = osc
        self.filenames = filenames
        self.personal = personal
        self.pressed.connect(self.clicked)
    
    def clicked(self):
        asyncio.run(main(
            self.osc,
            self.filenames,
            self.personal
        ))
        
        dlg = QMessageBox(self)
        dlg.setWindowTitle("Load All")
        dlg.setText("All Settings Loaded")
        dlg.exec()

        self.setDown(False)
        
async def main(osc, filenames, personal):
    for chName in filenames:
        if (filenames[chName].currentText() != ""):
            if (os.path.exists("data/" + filenames[chName].currentText())):
                await runSingle(osc, filenames[chName].currentText(), True)
                personal[chName].setCurrentText(filenames[chName].currentText().split(".")[0].split("_")[2])
            else:
                print("Invalid filename for " + chName)