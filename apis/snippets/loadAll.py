from apis.snippets.loadSingle import loadSingleNumSettings, runSingle
import os.path
from PyQt6.QtWidgets import (
    QPushButton,
)
import traceback
from util.customWidgets import ProgressDialog

class LoadAllButton(QPushButton):
    def __init__(self, config, osc, filenames, personal):
        super().__init__("Load All")
        self.config = config
        self.osc = osc
        self.filenames = filenames
        self.personal = personal
        self.pressed.connect(self.clicked)
    
    def clicked(self):
        dlg = ProgressDialog("All Settings Load", self.main)
        dlg.exec()

        self.setDown(False)
        
    def main(self, dlg):
        try:
            dlg.initBar.emit(loadAllNumSettings(self.filenames))
            for chName in self.filenames:
                if (self.filenames[chName].currentText() != ""):
                    if (os.path.exists("data/" + self.filenames[chName].currentText())):
                        runSingle(self.config, self.osc, "data/" + self.filenames[chName].currentText(), chName != "Mains", chName, dlg)
                        self.personal[chName].setCurrentText(self.filenames[chName].currentText().split(".")[0].split("_")[2])
                    else:
                        print("Invalid filename for " + chName)
            dlg.complete.emit()
        except Exception as ex:
            print(traceback.format_exc())
            dlg.raiseException.emit(ex)

def loadAllNumSettings(filenames):
    num = 0
    for chName in filenames:
        if (filenames[chName].currentText() != "" and os.path.exists("data/" + filenames[chName].currentText())):
            num = num + loadSingleNumSettings(filenames[chName].currentText(), chName != "Mains")
    return num