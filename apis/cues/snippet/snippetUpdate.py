import asyncio
import sys

from apis.snippets.saveSingle import getSetting

sys.path.insert(0, '../')

from PyQt6.QtWidgets import (
    QMessageBox,
    QPushButton,
)

class SnippetUpdateButton(QPushButton):
    def __init__(self, osc, textbox):
        super().__init__("Update Listed Settings")
        self.osc = osc
        self.textbox = textbox
        self.pressed.connect(self.clicked)
    
    def clicked(self):
        asyncio.run(main(
            self.osc,
            self.textbox
        ))

        dlg = QMessageBox(self)
        dlg.setWindowTitle("Snippet Update")
        dlg.setText("Update with Current Settings!")
        dlg.exec()

        self.setDown(False)

async def main(osc, textbox):
    curSettings = textbox.toPlainText().splitlines()
    textbox.clear()
    for line in curSettings:
        components = line.strip().split()

        if (components[0] == "foh"):
            textbox.append(await getSetting("foh", osc["fohClient"], osc["server"], components[1]))
        elif (components[0] == "iem"):
            textbox.append(await getSetting("iem", osc["iemClient"], osc["server"], components[1]))