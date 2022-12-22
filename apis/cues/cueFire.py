from apis.snippets.loadSingle import runSingle
import mido
import os.path
from PyQt6.QtWidgets import (
    QMessageBox,
    QPushButton,
)
import traceback
from util.constants import KEYS

class CueFireButton(QPushButton):
    def __init__(self, config, osc, prevIndex, index, printIndex, cues):
        super().__init__("Fire")
        if (len(printIndex) == 1):
            super().setShortcut("ctrl+" + printIndex)
        elif (printIndex == "10"):
            super().setShortcut("ctrl+0")

        self.config = config
        self.osc = osc
        self.prevIndex = prevIndex
        self.index = index
        self.printIndex = printIndex
        self.cues = cues
        self.pressed.connect(self.clicked)
        self.setFixedWidth(50)
    
    def clicked(self):
        try:
            main(
                self.config,
                self.osc,
                self.prevIndex,
                self.index,
                self.cues
            )
        except Exception as ex:
            print(traceback.format_exc())
            dlg = QMessageBox(self)
            dlg.setWindowTitle("Cue")
            dlg.setText("Error: " + str(ex))
            dlg.exec()

        self.setDown(False)

def main(config, osc, prevIndex, index, cues):
    if prevIndex[0] is not None:
        cues[prevIndex[0]]["label"].setStyleSheet("")
    prevIndex[0] = index
    try:
        if cues[index]["key"].currentText() != "":
            val = int((KEYS.index(cues[index]["key"].currentText()) * 127) / 11)

            #osc["audioMidi"].send(mido.Message("control_change", channel = 1, control = 100, value = 127)) # On/Off Message
            osc["audioMidi"].send(mido.Message("control_change", channel = 1, control = 101, value = val)) # Key Message
            osc["audioMidi"].send(mido.Message("control_change", channel = 1, control = 102, value = 127)) # Type Message

        if cues[index]["lead"].currentText() != "":
            bkgdVox = ["05", "06", "07", "08"] # TODO: Move this to config
            leadVox = ""
            if cues[index]["lead"].currentText() == "1":
                leadVox = "05"
                bkgdVox.remove(leadVox)
            elif cues[index]["lead"].currentText() == "2":
                leadVox = "06"
                bkgdVox.remove(leadVox)
            elif cues[index]["lead"].currentText() == "3":
                leadVox = "07"
                bkgdVox.remove(leadVox)
            elif cues[index]["lead"].currentText() == "4":
                leadVox = "08"
                bkgdVox.remove(leadVox)
            
            settings = {}
            settings["/ch/" + leadVox + "/mix/01/on"] = 1
            settings["/ch/" + leadVox + "/mix/02/on"] = 1
            settings["/ch/" + leadVox + "/mix/03/on"] = 0
            for ch in bkgdVox:
                settings["/ch/" + ch + "/mix/01/on"] = 0
                settings["/ch/" + ch + "/mix/02/on"] = 0
                settings["/ch/" + ch + "/mix/03/on"] = 1
            osc["fohClient"].bulk_send_messages(settings)
        
        if cues[index]["snippet"].filename != "":
            if os.path.exists(cues[index]["snippet"].filename):
                runSingle(config, osc, cues[index]["snippet"].filename)

        cues[index]["label"].setStyleSheet("color:green")
    except Exception as ex:
        cues[index]["label"].setStyleSheet("color:red")
        raise ex