from datetime import date, timedelta
from PyQt6.QtWidgets import (
    QFileDialog,
    QPushButton,
)

class CueSaveButton(QPushButton):
    def __init__(self, config, widgets):
        super().__init__("Save Set")
        self.config = config
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
                saveCue(self.config, file, self.widgets)
        
        self.setDown(False)

def saveCue(config, file, widgets):
    categories = list(config["cues"]["cueOptions"])
    file.write("cueHeaders")
    for category in categories:
        file.write("\t" + category)
    file.write("\tsnippet")

    for cue in widgets["cues"]:
        file.write("\n" + "cue")
        for category in categories:
            value = cue[category].currentText()
            if value == "":
                value = "N"
            file.write("\t" + value)
        value = cue["snippet"].filename
        if value == "":
            value = "N"
        file.write("\t" + value)
    
    for fader in widgets["faders"]:
        for command in fader["commands"]:
            file.write("\n" + "fader\t" + command + "\t" + fader["name"].text())