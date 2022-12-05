import os.path
import sys
import traceback
sys.path.insert(0, '../')

from apis.snippets.loadSingle import runSingle
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
        try:
            main(
                self.osc,
                self.filenames,
                self.personal
            )
            
            dlg = QMessageBox(self)
            dlg.setWindowTitle("Load All")
            dlg.setText("All Settings Loaded")
            dlg.exec()
        except Exception as ex:
            print(traceback.format_exc())
            dlg = QMessageBox(self)
            dlg.setWindowTitle("Load All")
            dlg.setText("Error: " + str(ex))
            dlg.exec()

        self.setDown(False)
        
def main(osc, filenames, personal):
    for chName in filenames:
        if (filenames[chName].currentText() != ""):
            if (os.path.exists("data/" + filenames[chName].currentText())):
                runSingle(osc, filenames[chName].currentText(), True)
                personal[chName].setCurrentText(filenames[chName].currentText().split(".")[0].split("_")[2])
            else:
                print("Invalid filename for " + chName)