import os.path
import sys
import traceback
sys.path.insert(0, '../')

from apis.snippets.loadSingle import runSingle
import mido
from util.constants import KEYS
from PyQt6.QtWidgets import (
    QMessageBox,
    QPushButton,
)

RESET_MSGS = {}

for ch in range(1, 4):
    RESET_MSGS["/ch/" + str(ch).zfill(2) + "/mix/fader"] = 0.75
    RESET_MSGS["/ch/" + str(ch).zfill(2) + "/mix/pan"] = 0.5
    RESET_MSGS["/ch/" + str(ch).zfill(2) + "/mix/on"] = 1

for ch in range(4, 24):
    RESET_MSGS["/ch/" + str(ch).zfill(2) + "/mix/fader"] = 0
    RESET_MSGS["/ch/" + str(ch).zfill(2) + "/mix/pan"] = 0.5

RESET_MSGS["/ch/24/mix/fader"] = 0.75
RESET_MSGS["/ch/24/mix/on"] = 1
RESET_MSGS["/ch/24/mix/pan"] = 0.5

for ch in range(25, 27):
    RESET_MSGS["/ch/" + str(ch).zfill(2) + "/mix/fader"] = 0
    RESET_MSGS["/ch/" + str(ch).zfill(2) + "/mix/pan"] = 0.5

RESET_MSGS["/ch/27/mix/fader"] = 0
RESET_MSGS["/ch/27/mix/pan"] = 0.0
RESET_MSGS["/ch/28/mix/pan"] = 1.0

for ch in range(29, 31):
    RESET_MSGS["/ch/" + str(ch).zfill(2) + "/mix/fader"] = 0
    RESET_MSGS["/ch/" + str(ch).zfill(2) + "/mix/pan"] = 0.5
    RESET_MSGS["/ch/" + str(ch).zfill(2) + "/mix/on"] = 1

RESET_MSGS["/ch/31/mix/fader"] = 0.75
RESET_MSGS["/ch/31/mix/on"] = 1
RESET_MSGS["/ch/31/mix/pan"] = 0.0
RESET_MSGS["/ch/32/mix/pan"] = 1.0
RESET_MSGS["/ch/31/mix/13/on"] = 1
RESET_MSGS["/ch/31/mix/13/level"] = 0.75
RESET_MSGS["/ch/31/mix/13/pan"] = 0.0
RESET_MSGS["/ch/32/mix/13/pan"] = 1.0

RESET_MSGS["/auxin/01/mix/fader"] = 0.5
RESET_MSGS["/auxin/01/mix/on"] = 1
RESET_MSGS["/auxin/01/mix/pan"] = 0.25
RESET_MSGS["/auxin/02/mix/pan"] = 0.75

RESET_MSGS["/auxin/03/mix/fader"] = 0.75
RESET_MSGS["/auxin/03/mix/on"] = 1
RESET_MSGS["/auxin/03/mix/pan"] = 0.25
RESET_MSGS["/auxin/04/mix/pan"] = 0.75

RESET_MSGS["/auxin/05/mix/fader"] = 0.75
RESET_MSGS["/auxin/05/mix/on"] = 1
RESET_MSGS["/auxin/05/mix/pan"] = 0.25
RESET_MSGS["/auxin/06/mix/pan"] = 0.75
RESET_MSGS["/auxin/05/mix/13/on"] = 1
RESET_MSGS["/auxin/05/mix/13/level"] = 0.75
RESET_MSGS["/auxin/05/mix/13/pan"] = 0.0
RESET_MSGS["/auxin/06/mix/13/pan"] = 1.0

for fx in range(0, 4):
    RESET_MSGS["/fxrtn/" + str((fx * 2) + 1).zfill(2) + "/mix/fader"] = 0.75
    RESET_MSGS["/fxrtn/" + str((fx * 2) + 1).zfill(2) + "/mix/on"] = 1
    RESET_MSGS["/fxrtn/" + str((fx * 2) + 1).zfill(2) + "/mix/pan"] = 0.0
    RESET_MSGS["/fxrtn/" + str((fx * 2) + 2).zfill(2) + "/mix/pan"] = 1.0

for bus in [1, 2, 7, 8]:
    RESET_MSGS["/bus/" + str(bus).zfill(2) + "/mix/fader"] = 0.75
    RESET_MSGS["/bus/" + str(bus).zfill(2) + "/mix/on"] = 1
    RESET_MSGS["/bus/" + str(bus).zfill(2) + "/mix/pan"] = 0.5
    RESET_MSGS["/bus/" + str(bus).zfill(2) + "/mix/03/on"] = 1
    RESET_MSGS["/bus/" + str(bus).zfill(2) + "/mix/03/level"] = 0.75
    RESET_MSGS["/bus/" + str(bus).zfill(2) + "/mix/03/pan"] = 0.5

for bus in [3, 5, 9, 13]:
    RESET_MSGS["/bus/" + str(bus).zfill(2) + "/mix/fader"] = 0.75
    RESET_MSGS["/bus/" + str(bus).zfill(2) + "/mix/on"] = 1
    RESET_MSGS["/bus/" + str(bus).zfill(2) + "/mix/pan"] = 0.0
    RESET_MSGS["/bus/" + str(bus + 1).zfill(2) + "/mix/pan"] = 1.0
    RESET_MSGS["/bus/" + str(bus).zfill(2) + "/mix/03/on"] = 1
    RESET_MSGS["/bus/" + str(bus).zfill(2) + "/mix/03/level"] = 0.75
    RESET_MSGS["/bus/" + str(bus).zfill(2) + "/mix/03/pan"] = 0.0
    RESET_MSGS["/bus/" + str(bus + 1).zfill(2) + "/mix/03/pan"] = 1.0

RESET_MSGS["/bus/11/mix/fader"] = 0.75
RESET_MSGS["/bus/11/mix/on"] = 1
RESET_MSGS["/bus/11/mix/pan"] = 0.5
RESET_MSGS["/bus/11/mix/pan"] = 0.0
RESET_MSGS["/bus/12/mix/pan"] = 1.0

for bus in [15, 16]:
    RESET_MSGS["/bus/" + str(bus).zfill(2) + "/mix/fader"] = 0.75
    RESET_MSGS["/bus/" + str(bus).zfill(2) + "/mix/on"] = 1
    RESET_MSGS["/bus/" + str(bus).zfill(2) + "/mix/pan"] = 0.5

for mtx in range(1, 7):
    RESET_MSGS["/mtx/" + str(mtx).zfill(2) + "/mix/fader"] = 0.75
    RESET_MSGS["/mtx/" + str(mtx).zfill(2) + "/mix/on"] = 1

RESET_MSGS["/main/st/mix/fader"] = 0
RESET_MSGS["/main/st/mix/on"] = 1
RESET_MSGS["/main/m/mix/fader"] = 0.75
RESET_MSGS["/main/m/mix/on"] = 1

for dca in range(1, 5):
    RESET_MSGS["/dca/" + str(dca) + "/fader"] = 0.75
    RESET_MSGS["/dca/" + str(dca) + "/on"] = 0

for dca in range(5, 7):
    RESET_MSGS["/dca/" + str(dca) + "/fader"] = 0.75
    RESET_MSGS["/dca/" + str(dca) + "/on"] = 1

RESET_MSGS["/dca/7/fader"] = 0.5
RESET_MSGS["/dca/7/on"] = 1
RESET_MSGS["/dca/8/fader"] = 0
RESET_MSGS["/dca/8/on"] = 1

class CueFireButton(QPushButton):
    def __init__(self, osc, prevIndex, index, printIndex, cues):
        super().__init__("Fire")
        if (len(printIndex) == 1):
            super().setShortcut("ctrl+" + printIndex)
        elif (printIndex == "10"):
            super().setShortcut("ctrl+0")

        self.osc = osc
        self.prevIndex = prevIndex
        self.index = index
        self.printIndex = printIndex
        self.cues = cues
        self.pressed.connect(self.clicked)
    
    def clicked(self):
        try:
            main(
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

def main(osc, prevIndex, index, cues):
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
            bkgdVox = ["05", "06", "07", "08"]
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
        
        if cues[index]["snippet"].text() == "RESET":
            reset(osc)
        elif cues[index]["snippet"].text() != "":
            if os.path.exists("data/" + cues[index]["snippet"].text()):
                runSingle(osc, cues[index]["snippet"].text(), False)

        cues[index]["label"].setStyleSheet("color:green")
    except Exception as ex:
        cues[index]["label"].setStyleSheet("color:red")
        raise ex

# This is specific to GP Seattle
def reset(osc):
    osc["fohClient"].bulk_send_messages(RESET_MSGS)

    # Reset Auto-Tune
    #midiPort.send(mido.Message("control_change", channel = 1, control = 100, value = 127)) # On/Off Message
    osc["audioMidi"].send(mido.Message("control_change", channel = 1, control = 101, value = 0)) # Key Message
    osc["audioMidi"].send(mido.Message("control_change", channel = 1, control = 102, value = 0)) # Type Message