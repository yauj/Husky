from apis.snippets.loadSingle import fireLines
import logging
from PyQt6.QtWidgets import (
    QPushButton,
)
import traceback
from util.customWidgets import ProgressDialog

logger = logging.getLogger(__name__)

class ResetButton(QPushButton):
    def __init__(self, config, osc):
        super().__init__("Reset Faders to Default")
        self.config = config
        self.osc = osc
        self.pressed.connect(self.clicked)
    
    def clicked(self):
        dlg = ProgressDialog("Mute, Pan, Fader settings reset", self.main)
        dlg.exec()

        self.setDown(False)

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