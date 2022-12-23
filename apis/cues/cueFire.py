from apis.snippets.loadSingle import fireLines, runSingle
import os.path
from PyQt6.QtWidgets import (
    QMessageBox,
    QPushButton,
)
import traceback

class CueFireButton(QPushButton):
    def __init__(self, config, osc, prevIndex, index, printIndex, cues):
        super().__init__("Fire")
        if (len(printIndex) == 1):
            super().setShortcut("ctrl+" + printIndex)
        elif (printIndex == "10"):
            super().setShortcut("ctrl+0")

        self.config = config
        self.osc = osc
        self.prevIndex = prevIndex
        self.index = index
        self.cues = cues
        self.pressed.connect(self.clicked)
        self.setFixedWidth(50)
    
    def clicked(self):
        try:
            main(
                self.config,
                self.osc,
                self.prevIndex,
                self.index,
                self.cues
            )
        except Exception as ex:
            print(traceback.format_exc())
            dlg = QMessageBox(self)
            dlg.setWindowTitle("Cue")
            dlg.setText("Error: " + str(ex))
            dlg.exec()

        self.setDown(False)

def main(config, osc, prevIndex, index, cues):
    if prevIndex[0] is not None:
        cues[prevIndex[0]]["label"].setStyleSheet("")
    prevIndex[0] = index
    try:
        for category in config["cues"]["cueOptions"]:
            if cues[index][category].currentText() != "":
                fireLines(config, osc, config["cues"]["cueOptions"][category][cues[index][category].currentText()])
        
        if cues[index]["snippet"].filename != "":
            if os.path.exists(cues[index]["snippet"].filename):
                runSingle(config, osc, cues[index]["snippet"].filename)

        cues[index]["label"].setStyleSheet("color:green")
    except Exception as ex:
        cues[index]["label"].setStyleSheet("color:red")
        raise ex