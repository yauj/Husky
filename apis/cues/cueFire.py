from apis.snippets.loadSingle import fireLines, loadSingleNumSettings, runSingle
import logging
import os.path
from PyQt6.QtWidgets import (
    QMessageBox,
    QPushButton,
)
import traceback
from util.customWidgets import ProgressDialog

logger = logging.getLogger(__name__)

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
            self.main()
        except Exception as ex:
            logger.error(traceback.format_exc())
            dlg = QMessageBox(self)
            dlg.setWindowTitle("Cue")
            dlg.setText("Error: " + str(ex))
            dlg.exec()

        self.setDown(False)

    def main(self):
        if self.prevIndex[0] is not None:
            self.cues[self.prevIndex[0]]["label"].setStyleSheet("")
        self.prevIndex[0] = self.index
        try:
            for category in self.config["cues"]["cueOptions"]:
                if self.cues[self.index][category].currentText() != "":
                    fireLines(self.config, self.osc, self.config["cues"]["cueOptions"][category][self.cues[self.index][category].currentText()])
            
            if self.cues[self.index]["snippet"].filename != "":
                if os.path.exists(self.cues[self.index]["snippet"].filename):
                    self.snippetNumSettings = loadSingleNumSettings(self.config, self.cues[self.index]["snippet"].filename)
                    if self.snippetNumSettings >= 100: # Will take more than 1 second
                        dlg = ProgressDialog("Snippet Load", self.loadSnippet)
                        dlg.exec()
                    else:
                        self.loadSnippet()

            self.cues[self.index]["label"].setStyleSheet("color:green")
        except Exception as ex:
            self.cues[self.index]["label"].setStyleSheet("color:red")
            raise ex

    def loadSnippet(self, dlg = None):
        if dlg is not None:
            dlg.initBar.emit(self.snippetNumSettings)
        runSingle(self.config, self.osc, self.cues[self.index]["snippet"].filename, dlg = dlg)
        if dlg is not None:
            dlg.close()