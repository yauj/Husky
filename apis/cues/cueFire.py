from apis.snippets.loadSingle import fireLines, loadSingleNumSettings, runSingle
import logging
import os.path
from PyQt6.QtWidgets import (
    QMessageBox,
    QPushButton,
)
import traceback

logger = logging.getLogger(__name__)

class CueFireButton(QPushButton):
    def __init__(self, config, osc, prevIndex, index, printIndex, cues, progressBar):
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
        self.progressBar = progressBar
        self.pressed.connect(self.clicked)
        self.setFixedWidth(50)
    
    def clicked(self):
        self.main()

        self.setDown(False)

    def main(self):
        if self.prevIndex[0] is not None:
            self.cues[self.prevIndex[0]]["label"].setStyleSheet("")
        self.prevIndex[0] = self.index
        try:
            self.progressBar.initBar.emit(1)
            for category in self.config["cues"]["cueOptions"]:
                if self.cues[self.index][category].currentText() != "":
                    fireLines(self.config, self.osc, self.config["cues"]["cueOptions"][category][self.cues[self.index][category].currentText()])
            
            if self.cues[self.index]["snippet"].filename != "":
                if os.path.exists(self.cues[self.index]["snippet"].filename):
                    self.snippetNumSettings = loadSingleNumSettings(self.config, self.cues[self.index]["snippet"].filename)
                    self.loadSnippet()

            self.cues[self.index]["label"].setStyleSheet("color:green")
            self.progressBar.complete.emit()
        except Exception as ex:
            logger.error(traceback.format_exc())
            self.cues[self.index]["label"].setStyleSheet("color:red")
            self.progressBar.raiseException.emit(ex)

    def loadSnippet(self):
        self.progressBar.initBar.emit(self.snippetNumSettings)
        runSingle(self.config, self.osc, self.cues[self.index]["snippet"].filename, dlg = self.progressBar)