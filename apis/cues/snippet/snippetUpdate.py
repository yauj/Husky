import sys
import traceback
sys.path.insert(0, '../')

from apis.snippets.saveSingle import getSetting
from PyQt6.QtWidgets import (
    QMessageBox,
    QPushButton,
)

class SnippetUpdateButton(QPushButton):
    def __init__(self, osc, textbox):
        super().__init__("Update Listed Settings")
        self.osc = osc
        self.textbox = textbox
        self.pressed.connect(self.clicked)
    
    def clicked(self):
        curSettings = self.textbox.toPlainText().splitlines()

        try:
            main(
                self.osc,
                curSettings,
                self.textbox
            )

            dlg = QMessageBox(self)
            dlg.setWindowTitle("Update Snippet")
            dlg.setText("Update with Current Settings!")
            dlg.exec()
        except Exception as ex:
            self.textbox.clear()
            for line in curSettings:
                self.textbox.append(line)

            print(traceback.format_exc())
            dlg = QMessageBox(self)
            dlg.setWindowTitle("Update Snippet")
            dlg.setText("Error: " + str(ex))
            dlg.exec()

        self.setDown(False)

def main(osc, curSettings, textbox):
    textbox.clear()
    for line in curSettings:
        components = line.strip().split()

        if (components[3] == "delta"):
            textbox.append(line.strip())
        else:
            if (components[0] == "foh"):
                textbox.append(getSetting("foh", osc["fohClient"], osc["server"], components[1]))
            elif (components[0] == "iem"):
                textbox.append(getSetting("iem", osc["iemClient"], osc["server"], components[1]))