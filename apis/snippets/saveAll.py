from apis.snippets.saveSingle import runSingle, saveSingleNumSettings
from PyQt6.QtWidgets import (
    QPushButton,
)
import traceback
from util.customWidgets import ProgressDialog

class SaveAllButton(QPushButton):
    def __init__(self, osc, personNames, config):
        super().__init__("Save All")
        self.osc = osc
        self.personNames = personNames
        self.config = config
        self.pressed.connect(self.clicked)
    
    def clicked(self):
        dlg = ProgressDialog("All Settings Sav", self.main)
        dlg.exec()

        self.setDown(False)
        
    def main(self, dlg):
        try:
            dlg.initBar.emit(saveAllNumSettings(self.personNames, self.config, self.osc))
            for chName in self.personNames:
                if (self.personNames[chName].currentText() != ""):
                    runSingle(self.osc, chName, self.personNames[chName].currentText(), self.config, dlg)
            dlg.complete.emit()
        except Exception as ex:
            print(traceback.format_exc())
            dlg.raiseException.emit(ex)

def saveAllNumSettings(personNames, config, osc):
    num = 0
    for chName in personNames:
        if (personNames[chName].currentText() != ""):
            num = num + saveSingleNumSettings(config, osc, chName)
    return num