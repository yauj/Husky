from apis.snippets.saveSingle import appendSettingsToTextbox
import logging
from PyQt6.QtWidgets import (
    QMessageBox,
    QPushButton,
)
import traceback

logger = logging.getLogger(__name__)

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

            logger.error(traceback.format_exc())
            dlg = QMessageBox(self)
            dlg.setWindowTitle("Update Snippet")
            dlg.setText("Error: " + str(ex))
            dlg.exec()

        self.setDown(False)

def main(osc, curSettings, textbox):
    fohSettings = {}
    iemSettings = {}
    otherLines = []
    for line in curSettings:
        components = line.strip().split()

        if components[0] == "foh":
            fohSettings[components[1]] = None
        elif components[0] == "iem":
            iemSettings[components[1]] = None
        else:
            otherLines.append(line)

    textbox.clear()
    appendSettingsToTextbox(osc, textbox, "foh", fohSettings)
    appendSettingsToTextbox(osc, textbox, "iem", iemSettings)
    for line in otherLines:
        textbox.append(line)