import sys
sys.path.insert(0, '../')

from apis.snippets.saveSingle import saveChannels, saveIEMBus
import asyncio
from datetime import date, timedelta
from PyQt6.QtWidgets import (
    QFileDialog,
    QPushButton,
)

class SnippetSaveButton(QPushButton):
    def __init__(self, widgets, osc, config, options, cue):
        super().__init__("Save New Snippet")
        self.widgets = widgets
        self.osc = osc
        self.config = config
        self.options = options
        self.cue = cue
        self.pressed.connect(self.clicked)
    
    def clicked(self):
        nextSun = (date.today() + timedelta(6 - date.today().weekday())).strftime("%Y%m%d")

        dlg = QFileDialog()
        dlg.setWindowTitle("Save Snippet")
        dlg.setAcceptMode(QFileDialog.AcceptMode.AcceptSave)
        dlg.setDirectory("data")
        dlg.selectFile(nextSun + "_SWS_?.osc")
        dlg.setDefaultSuffix(".osc") 
        if dlg.exec():
            asyncio.run(main(
                self.osc,
                self.config,
                self.options,
                dlg.selectedFiles()[0]
            ))

            if self.cue.currentText() != "":
                self.widgets["cue"][self.cue.currentText()].setText(dlg.selectedFiles()[0])

        self.setDown(False)
        
async def main(osc, config, options, filename):
    with open(filename, "w") as file:
        for chName in options:
            if "channels" in options[chName] and options[chName]["channels"].isChecked():
                await saveChannels(osc, file, config[chName]["channels"])

            if "iem_bus" in options[chName] and options[chName]["iem_bus"].isChecked():
                await saveIEMBus(osc, file, config[chName]["iem_bus"])
