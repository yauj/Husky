from apis.snippets.loadSingle import fireLines
import logging
from PyQt6.QtGui import (
    QAction,
)
from PyQt6.QtWidgets import (
    QMessageBox
)
import traceback
from util.customWidgets import ProgressDialog

logger = logging.getLogger(__name__)

class ResetCommands(QAction):
    def __init__(self, s, config, osc):
        super().__init__("Reset Commands", s)
        self.s = s
        self.config = config
        self.osc = osc
        self.triggered.connect(self.clicked)
    
    def clicked(self):
        dlg = QMessageBox(self.s)
        dlg.setWindowTitle("Reset Commands")
        dlg.setText("Are you sure you want to run reset commands?\nThese are the resetCommands specified in the config file.")
        dlg.setStandardButtons(QMessageBox.StandardButton.Ok | QMessageBox.StandardButton.Cancel)
        if dlg.exec() == QMessageBox.StandardButton.Ok:
            newDlg = ProgressDialog("Reset", self.main)
            newDlg.exec()

    def main(self, dlg):
        try:
            dlg.initBar.emit(len(self.config["resetCommands"]))

            self.osc["fohClient"].bulk_send_messages(self.config["resetCommands"], dlg)

            lines = []
            for category in self.config["cues"]["cueOptions"]:
                if "RESET" in self.config["cues"]["cueOptions"][category]:
                    lines.extend(self.config["cues"]["cueOptions"][category]["RESET"])

            fireLines(self.config, self.osc, lines)

            logger.info("Settings Reset")
            dlg.complete.emit()
        except Exception as ex:
            logger.exception(traceback.format_exc())
            dlg.raiseException.emit(ex)