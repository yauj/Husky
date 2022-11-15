import sys
sys.path.insert(0, '../')

from datetime import date
from PyQt6.QtWidgets import (
    QFileDialog,
    QPushButton,
)

class CueSaveButton(QPushButton):
    def __init__(self, cues):
        super().__init__("Save Set")
        self.cues = cues
        self.pressed.connect(self.clicked)
    
    def clicked(self):
        dlg = QFileDialog()
        dlg.setWindowTitle("Save Set")
        dlg.setAcceptMode(QFileDialog.AcceptMode.AcceptSave)
        dlg.setDirectory("data")
        dlg.selectFile(date.today().strftime("%Y%m%d") + "_")
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

                    file.write("\n" + key + " " + lead)