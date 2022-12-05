import sys
import traceback
sys.path.insert(0, '../')

from apis.snippets.saveSingle import runSingle
from PyQt6.QtWidgets import (
    QMessageBox,
    QPushButton,
)

class SaveAllButton(QPushButton):
    def __init__(self, widgets, osc, personNames, config):
        super().__init__("Save All")
        self.widgets = widgets
        self.osc = osc
        self.personNames = personNames
        self.config = config
        self.pressed.connect(self.clicked)
    
    def clicked(self):
        try:
            main(
                self.osc,
                self.personNames,
                self.config
            )
            
            dlg = QMessageBox(self)
            dlg.setWindowTitle("Save All")
            dlg.setText("All Settings Saved")
            dlg.exec()
        except Exception as ex:
            print(traceback.format_exc())
            dlg = QMessageBox(self)
            dlg.setWindowTitle("Save All")
            dlg.setText("Error: " + str(ex))
            dlg.exec() 

        self.setDown(False)
        
def main(osc, personNames, config):
    for chName in personNames:
        if (personNames[chName].currentText() != ""):
            runSingle(osc, chName + "_" + personNames[chName].currentText(), config[chName])
