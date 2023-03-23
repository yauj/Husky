from apis.snippets.saveSingle import appendSettingsToTextbox
import logging
from PyQt6.QtWidgets import (
    QMessageBox,
    QPushButton,
)
import traceback

logger = logging.getLogger(__name__)

class SnippetUpdateButton(QPushButton):
    def __init__(self, osc, widgets, textbox):
        super().__init__("Update Listed Settings")
        self.osc = osc
        self.widgets = widgets
        self.textbox = textbox
        self.pressed.connect(self.clicked)
    
    def clicked(self):
        curSettings = self.textbox.toPlainText().splitlines()

        try:
            main(
                self.osc,
                self.widgets,
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

def main(osc, widgets, curSettings, textbox):
    fohSettings = {}
    iemSettings = {}
    luckySettings = {}
    otherLines = []
    for line in curSettings:
        components = line.strip().split()

        if components[0] == "foh":
            fohSettings[components[1]] = None
        elif components[0] == "iem":
            iemSettings[components[1]] = None
        elif components[0] == "lucky":
            luckySettings[components[1]] = line
        else:
            otherLines.append(line)

    textbox.clear()
    if len(fohSettings) > 0:
        appendSettingsToTextbox(osc, textbox, "foh", fohSettings)
    if len(iemSettings) > 0:
        appendSettingsToTextbox(osc, textbox, "iem", iemSettings)
    updateLucky(widgets, textbox, luckySettings)
    for line in otherLines:
        textbox.append(line)

def updateLucky(widgets, textbox, settings):
    for channel in settings:
        if "AutoMixLucky" in widgets["windows"]:
            if channel in widgets["windows"]["AutoMixLucky"].assignments:
                current = widgets["windows"]["AutoMixLucky"].assignments[channel].currentText()
                textbox.append("lucky " + channel + " " + current)
        else: # Keep existing line if window not open
            textbox.append(settings[channel])