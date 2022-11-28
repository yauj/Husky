import os
import sys
sys.path.insert(0, '../')

from apis.snippets.saveSingle import saveChannels, saveIEMBus, saveSetting
import asyncio
from datetime import date, timedelta
from PyQt6.QtWidgets import (
    QFileDialog,
    QMessageBox,
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
            try:
                asyncio.run(main(
                    self.osc,
                    self.config,
                    self.options,
                    dlg.selectedFiles()[0]
                ))

                if self.cue.currentText() != "":
                    self.widgets["cue"][self.cue.currentText()].setText(dlg.selectedFiles()[0])
            except Exception as ex:
                os.remove(dlg.selectedFiles()[0])
                
                print(ex)
                dlg = QMessageBox(self)
                dlg.setWindowTitle("Save Snippet")
                dlg.setText("Error: " + str(ex))
                dlg.exec()

        self.setDown(False)
        
async def main(osc, config, options, filename):
    with open(filename, "w") as file:
        for chName in options["personal"]:
            if "channels" in options["personal"][chName] and options["personal"][chName]["channels"].isChecked():
                await saveChannels(osc, file, config["personal"][chName]["channels"])

            if "iem_bus" in options["personal"][chName] and options["personal"][chName]["iem_bus"].isChecked():
                await saveIEMBus(osc, file, config["personal"][chName]["iem_bus"])

        for name in options["settings"]:
            if options["settings"][name].isChecked():
                for setting in config["settings"][name]:
                    await saveSetting(file, "foh", osc["fohClient"], osc["server"], setting)