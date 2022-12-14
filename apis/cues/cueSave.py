from datetime import date, timedelta
from PyQt6.QtWidgets import (
    QFileDialog,
    QPushButton,
)

class CueSaveButton(QPushButton):
    def __init__(self, widgets):
        super().__init__("Save Set")
        self.widgets = widgets
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
                saveCue(file, self.widgets)
        
        self.setDown(False)

def saveCue(file, widgets):
    for cue in widgets["cues"]:
        key = cue["key"].currentText()
        if key == "":
            key = "N"

        lead = cue["lead"].currentText()
        if lead == "":
            lead = "N"

        snippet = cue["snippet"].filename
        if snippet == "":
            snippet = "N"

        file.write("\n" + "cue " + key + " " + lead + " " + snippet)
    
    for fader in widgets["faders"]:
        for command in fader["commands"]:
            file.write("\n" + "fader " + command + " " + fader["name"].text())