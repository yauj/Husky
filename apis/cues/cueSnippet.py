import sys
sys.path.insert(0, '../')

from apis.snippets.saveSingle import saveChannels, saveIEMBus
import asyncio
from datetime import date
from util.defaultOSC import SimpleClient
from PyQt6.QtWidgets import (
    QMessageBox,
    QPushButton,
)

class CueSnippetButton(QPushButton):
    def __init__(self, widgets, server, config, options, cue):
        super().__init__("Save New Snippet")
        self.widgets = widgets
        self.server = server
        self.config = config
        self.options = options
        self.cue = cue
        self.pressed.connect(self.clicked)
    
    def clicked(self):
        filename = date.today().strftime("%Y%m%d") + "_Cue_" + self.cue.currentText() + ".osc"

        asyncio.run(main(
            SimpleClient(self.widgets["ip"]["FOH"].text()),
            SimpleClient(self.widgets["ip"]["IEM"].text()),
            self.server,
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
        
async def main(fohClient, iemClient, server, config, options, filename):
    fohClient._sock = server.socket
    iemClient._sock = server.socket

    with open("data/" + filename, "w") as file:
        for chName in options:
            if "channels" in options[chName] and options[chName]["channels"].isChecked():
                await saveChannels(fohClient, server, file, config[chName]["channels"])

            if "iem_bus" in options[chName] and options[chName]["iem_bus"].isChecked():
                await saveIEMBus(iemClient, server, file, config[chName]["iem_bus"])
