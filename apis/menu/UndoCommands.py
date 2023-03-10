import logging
from PyQt6.QtGui import (
    QAction,
)
import traceback
from util.customWidgets import ProgressDialog

logger = logging.getLogger(__name__)

class UndoCommands(QAction):
    def __init__(self, s, osc, mixerName):
        super().__init__(mixerName.upper() + " Mixer", s)
        self.s = s
        self.osc = osc
        self.mixerName = mixerName
        self.triggered.connect(self.onTrigger)

    def onTrigger(self):
        dlg = ProgressDialog("Undo", self.main)
        dlg.exec()
    
    def main(self, dlg):
        try:
            if self.osc[self.mixerName + "Client"].undo(dlg):
                message = "Successfully undid previously applied commands"
            else:
                message = "No previous commands to undo."
            dlg.completeWithMessage.emit(message)
        except Exception as ex:
            logger.error(traceback.format_exc())
            dlg.raiseException.emit(ex)