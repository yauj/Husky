from apis.snippets.saveSingle import appendSettingsToTextbox
import logging
from PyQt6.QtWidgets import (
    QMessageBox,
    QPushButton,
)
import traceback

logger = logging.getLogger(__name__)

class SnippetUpdateButton(QPushButton):
    def __init__(self, config, osc, widgets, textbox):
        super().__init__("Update Listed Settings")
        self.config = config
        self.osc = osc
        self.widgets = widgets
        self.textbox = textbox
        self.pressed.connect(self.clicked)
    
    def clicked(self):
        curSettings = self.textbox.toPlainText().splitlines()

        try:
            main(
                self.config,
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

def main(config, osc, widgets, curSettings, textbox):
    fohSettings = {}
    iemSettings = {}
    midiSettings = {}
    luckySettings = {}
    otherLines = []
    for line in curSettings:
        components = line.strip().split()

        if components[0] == "foh":
            fohSettings[components[1]] = None
        elif components[0] == "iem":
            iemSettings[components[1]] = None
        elif components[0] == "midi":
            if components[1] not in midiSettings:
                midiSettings[components[1]] = []
            midiSettings[components[1]].append(components)
        elif components[0] == "lucky":
            luckySettings[components[1]] = line
        else:
            otherLines.append(line)

    textbox.clear()
    if len(fohSettings) > 0:
        appendSettingsToTextbox(osc, textbox, "foh", fohSettings)
    if len(iemSettings) > 0:
        appendSettingsToTextbox(osc, textbox, "iem", iemSettings)
    for target in midiSettings:
        if target in config["midi"] and config["midi"][target]["type"] == "cc":
            updateMidi(osc, midiSettings[target])

        for components in midiSettings[target]:
            textbox.append(" ".join(components))
    updateLucky(widgets, textbox, luckySettings)
    for line in otherLines:
        textbox.append(line)

def updateMidi(osc, settings):
    for components in settings:
        channel = int(components[2]) - 1
        control = int(components[3])
        if channel in osc["virtualMidi"].history:
            if control in osc["virtualMidi"].history[channel]:
                components[4] = str(osc["virtualMidi"].history[channel][control])
                

def updateLucky(widgets, textbox, settings):
    for channel in settings:
        if "AutoMixLucky" in widgets["windows"]:
            if channel in widgets["windows"]["AutoMixLucky"].assignments:
                assignment = widgets["windows"]["AutoMixLucky"].assignments[channel].currentText()
                # Don't save weights, since weights should just help match mic sensitivities, so shouldn't be dependent on person.
                # channelIdx = int(channel.replace("/ch/", "")) - 1
                # weight = widgets["windows"]["AutoMixLucky"].weights[channelIdx].value()
                textbox.append("lucky " + channel + " " + assignment)
        else: # Keep existing line if window not open
            textbox.append(settings[channel])