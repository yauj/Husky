import sys
sys.path.insert(0, '../')

from datetime import date, timedelta
from PyQt6.QtWidgets import (
    QFileDialog,
    QPushButton,
)

class CueSaveButton(QPushButton):
    def __init__(self, cues, faderNames, faders):
        super().__init__("Save Set")
        self.cues = cues
        self.faderNames = faderNames
        self.faders = faders
        self.pressed.connect(self.clicked)
    
    def clicked(self):
        nextSun = (date.today() + timedelta(6 - date.today().weekday())).strftime("%Y%m%d")

        dlg = QFileDialog()
        dlg.setWindowTitle("Save Set")
        dlg.setAcceptMode(QFileDialog.AcceptMode.AcceptSave)
        dlg.setDirectory("data")
        dlg.selectFile(nextSun + "_SWS.cue")
        dlg.setDefaultSuffix(".cue") 
        if dlg.exec():
            with open(dlg.selectedFiles()[0], "w") as file:
                for cue in self.cues:
                    key = cue["key"].currentText()
                    if key == "":
                        key = "N"

                    lead = cue["lead"].currentText()
                    if lead == "":
                        lead = "N"

                    snippet = cue["snippet"].text()
                    if snippet == "":
                        snippet = "N"

                    file.write("\n" + "cue " + key + " " + lead + " " + snippet)
                
                for i in range(0, len(self.faderNames)):
                    for command in self.faders[i]:
                        file.write("\n" + "fader " + command + " " + self.faderNames[i].text())
        
        self.setDown(False)