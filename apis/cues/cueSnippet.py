import sys
sys.path.insert(0, '../')

from apis.snippets.saveSingle import saveChannels, saveIEMBus
import asyncio
from datetime import date
from PyQt6.QtWidgets import (
    QMessageBox,
    QPushButton,
)

class CueSnippetButton(QPushButton):
    def __init__(self, widgets, osc, config, options, cue):
        super().__init__("Save New Snippet")
        self.widgets = widgets
        self.osc = osc
        self.config = config
        self.options = options
        self.cue = cue
        self.pressed.connect(self.clicked)
    
    def clicked(self):
        filename = date.today().strftime("%Y%m%d") + "_Cue_" + self.cue.currentText() + ".osc"

        asyncio.run(main(
            self.osc,
            self.config,
            self.options,
            filename
        ))
        
        if self.cue.currentText() != "":
            self.widgets["cue"][self.cue.currentText()].setText(filename)
        
        dlg = QMessageBox(self)
        dlg.setWindowTitle("Cue Snippet")
        dlg.setText("Snippet Saved for cue " + self.cue.currentText())
        dlg.exec()
        
async def main(osc, config, options, filename):
    with open("data/" + filename, "w") as file:
        for chName in options:
            if "channels" in options[chName] and options[chName]["channels"].isChecked():
                await saveChannels(osc, file, config[chName]["channels"])

            if "iem_bus" in options[chName] and options[chName]["iem_bus"].isChecked():
                await saveIEMBus(osc, file, config[chName]["iem_bus"])
