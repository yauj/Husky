import os.path
import sys
import traceback
sys.path.insert(0, '../')

from apis.snippets.loadSingle import runSingle
import asyncio
import mido
from util.constants import KEYS
from PyQt6.QtWidgets import (
    QMessageBox,
    QPushButton,
)

class CueFireButton(QPushButton):
    def __init__(self, widgets, osc, prevIndex, index, printIndex, cues):
        super().__init__("Fire")
        if (len(printIndex) == 1):
            super().setShortcut("ctrl+" + printIndex)
        elif (printIndex == "10"):
            super().setShortcut("ctrl+0")

        self.widgets = widgets
        self.osc = osc
        self.prevIndex = prevIndex
        self.index = index
        self.printIndex = printIndex
        self.cues = cues
        self.pressed.connect(self.clicked)
    
    def clicked(self):
        try:
            asyncio.run(main(
                self.osc,
                self.prevIndex,
                self.index,
                self.cues
            ))
        except Exception as ex:
            print(traceback.format_exc())
            dlg = QMessageBox(self)
            dlg.setWindowTitle("Cue")
            dlg.setText("Error: " + str(ex))
            dlg.exec()

        self.setDown(False)

async def main(osc, prevIndex, index, cues):
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
                
            await osc["fohClient"].send_message("/ch/" + leadVox + "/mix/01/on", 1)
            await osc["fohClient"].send_message("/ch/" + leadVox + "/mix/02/on", 1)
            await osc["fohClient"].send_message("/ch/" + leadVox + "/mix/03/on", 0)
            for ch in bkgdVox:
                await osc["fohClient"].send_message("/ch/" + ch + "/mix/01/on", 0)
                await osc["fohClient"].send_message("/ch/" + ch + "/mix/02/on", 0)
                await osc["fohClient"].send_message("/ch/" + ch + "/mix/03/on", 1)
        
        if cues[index]["snippet"].text() == "RESET":
            await reset(osc)
        elif cues[index]["snippet"].text() != "":
            if os.path.exists("data/" + cues[index]["snippet"].text()):
                await runSingle(osc, cues[index]["snippet"].text(), False)

        cues[index]["label"].setStyleSheet("color:green")
    except Exception as ex:
        cues[index]["label"].setStyleSheet("color:red")
        raise ex

# This is specific to GP Seattle
async def reset(osc):
    for ch in range(1, 4):
        await osc["fohClient"].send_message("/ch/" + str(ch).zfill(2) + "/mix/fader", 0.75)
        await osc["fohClient"].send_message("/ch/" + str(ch).zfill(2) + "/mix/pan", 0.5)
        await osc["fohClient"].send_message("/ch/" + str(ch).zfill(2) + "/mix/on", 1)

    for ch in range(4, 24):
        await osc["fohClient"].send_message("/ch/" + str(ch).zfill(2) + "/mix/fader", 0)
        await osc["fohClient"].send_message("/ch/" + str(ch).zfill(2) + "/mix/pan", 0.5)
    
    await osc["fohClient"].send_message("/ch/24/mix/fader", 0.75)
    await osc["fohClient"].send_message("/ch/24/mix/on", 1)
    await osc["fohClient"].send_message("/ch/24/mix/pan", 0.5)

    for ch in range(25, 27):
        await osc["fohClient"].send_message("/ch/" + str(ch).zfill(2) + "/mix/fader", 0)
        await osc["fohClient"].send_message("/ch/" + str(ch).zfill(2) + "/mix/pan", 0.5)
    
    await osc["fohClient"].send_message("/ch/27/mix/fader", 0)
    await osc["fohClient"].send_message("/ch/27/mix/pan", 0.0)
    await osc["fohClient"].send_message("/ch/28/mix/pan", 1.0)

    for ch in range(29, 31):
        await osc["fohClient"].send_message("/ch/" + str(ch).zfill(2) + "/mix/fader", 0)
        await osc["fohClient"].send_message("/ch/" + str(ch).zfill(2) + "/mix/pan", 0.5)
        await osc["fohClient"].send_message("/ch/" + str(ch).zfill(2) + "/mix/on", 1)

    await osc["fohClient"].send_message("/ch/31/mix/fader", 0.75)
    await osc["fohClient"].send_message("/ch/31/mix/on", 1)
    await osc["fohClient"].send_message("/ch/31/mix/pan", 0.0)
    await osc["fohClient"].send_message("/ch/32/mix/pan", 1.0)
    await osc["fohClient"].send_message("/ch/31/mix/13/on", 1)
    await osc["fohClient"].send_message("/ch/31/mix/13/level", 0.75)
    await osc["fohClient"].send_message("/ch/31/mix/13/pan", 0.0)
    await osc["fohClient"].send_message("/ch/32/mix/13/pan", 1.0)

    await osc["fohClient"].send_message("/auxin/01/mix/fader", 0.5)
    await osc["fohClient"].send_message("/auxin/01/mix/on", 1)
    await osc["fohClient"].send_message("/auxin/01/mix/pan", 0.25)
    await osc["fohClient"].send_message("/auxin/02/mix/pan", 0.75)

    await osc["fohClient"].send_message("/auxin/03/mix/fader", 0.75)
    await osc["fohClient"].send_message("/auxin/03/mix/on", 1)
    await osc["fohClient"].send_message("/auxin/03/mix/pan", 0.25)
    await osc["fohClient"].send_message("/auxin/04/mix/pan", 0.75)
    
    await osc["fohClient"].send_message("/auxin/05/mix/fader", 0.75)
    await osc["fohClient"].send_message("/auxin/05/mix/on", 1)
    await osc["fohClient"].send_message("/auxin/05/mix/pan", 0.25)
    await osc["fohClient"].send_message("/auxin/06/mix/pan", 0.75)
    await osc["fohClient"].send_message("/auxin/05/mix/13/on", 1)
    await osc["fohClient"].send_message("/auxin/05/mix/13/level", 0.75)
    await osc["fohClient"].send_message("/auxin/05/mix/13/pan", 0.0)
    await osc["fohClient"].send_message("/auxin/06/mix/13/pan", 1.0)

    for fx in range(0, 4):
        await osc["fohClient"].send_message("/fxrtn/" + str((fx * 2) + 1).zfill(2) + "/mix/fader", 0.75)
        await osc["fohClient"].send_message("/fxrtn/" + str((fx * 2) + 1).zfill(2) + "/mix/on", 1)
        await osc["fohClient"].send_message("/fxrtn/" + str((fx * 2) + 1).zfill(2) + "/mix/pan", 0.0)
        await osc["fohClient"].send_message("/fxrtn/" + str((fx * 2) + 2).zfill(2) + "/mix/pan", 1.0)

    for bus in [1, 2, 7, 8]:
        await osc["fohClient"].send_message("/bus/" + str(bus).zfill(2) + "/mix/fader", 0.75)
        await osc["fohClient"].send_message("/bus/" + str(bus).zfill(2) + "/mix/on", 1)
        await osc["fohClient"].send_message("/bus/" + str(bus).zfill(2) + "/mix/pan", 0.5)
        await osc["fohClient"].send_message("/bus/" + str(bus).zfill(2) + "/mix/03/on", 1)
        await osc["fohClient"].send_message("/bus/" + str(bus).zfill(2) + "/mix/03/level", 0.75)
        await osc["fohClient"].send_message("/bus/" + str(bus).zfill(2) + "/mix/03/pan", 0.5)

    for bus in [3, 5, 9, 13]:
        await osc["fohClient"].send_message("/bus/" + str(bus).zfill(2) + "/mix/fader", 0.75)
        await osc["fohClient"].send_message("/bus/" + str(bus).zfill(2) + "/mix/on", 1)
        await osc["fohClient"].send_message("/bus/" + str(bus).zfill(2) + "/mix/pan", 0.0)
        await osc["fohClient"].send_message("/bus/" + str(bus + 1).zfill(2) + "/mix/pan", 1.0)
        await osc["fohClient"].send_message("/bus/" + str(bus).zfill(2) + "/mix/03/on", 1)
        await osc["fohClient"].send_message("/bus/" + str(bus).zfill(2) + "/mix/03/level", 0.75)
        await osc["fohClient"].send_message("/bus/" + str(bus).zfill(2) + "/mix/03/pan", 0.0)
        await osc["fohClient"].send_message("/bus/" + str(bus + 1).zfill(2) + "/mix/03/pan", 1.0)
    
    await osc["fohClient"].send_message("/bus/11/mix/fader", 0.75)
    await osc["fohClient"].send_message("/bus/11/mix/on", 1)
    await osc["fohClient"].send_message("/bus/11/mix/pan", 0.5)
    await osc["fohClient"].send_message("/bus/11/mix/pan", 0.0)
    await osc["fohClient"].send_message("/bus/12/mix/pan", 1.0)

    for bus in [15, 16]:
        await osc["fohClient"].send_message("/bus/" + str(bus).zfill(2) + "/mix/fader", 0.75)
        await osc["fohClient"].send_message("/bus/" + str(bus).zfill(2) + "/mix/on", 1)
        await osc["fohClient"].send_message("/bus/" + str(bus).zfill(2) + "/mix/pan", 0.5)

    for mtx in (1, 7):
        await osc["fohClient"].send_message("/mtx/" + str(mtx).zfill(2) + "/mix/fader", 0.75)
        await osc["fohClient"].send_message("/mtx/" + str(mtx).zfill(2) + "/mix/on", 1)

    await osc["fohClient"].send_message("/main/st/mix/fader", 0)
    await osc["fohClient"].send_message("/main/st/mix/on", 1)
    await osc["fohClient"].send_message("/main/m/mix/fader", 0.75)
    await osc["fohClient"].send_message("/main/m/mix/on", 1)

    for dca in range(1, 5):
        await osc["fohClient"].send_message("/dca/" + str(dca) + "/fader", 0.75)
        await osc["fohClient"].send_message("/dca/" + str(dca) + "/on", 0)

    for dca in range(5, 7):
        await osc["fohClient"].send_message("/dca/" + str(dca) + "/fader", 0.75)
        await osc["fohClient"].send_message("/dca/" + str(dca) + "/on", 1)

    await osc["fohClient"].send_message("/dca/7/fader", 0.5)
    await osc["fohClient"].send_message("/dca/7/on", 1)
    await osc["fohClient"].send_message("/dca/8/fader", 0)
    await osc["fohClient"].send_message("/dca/8/on", 1)

    # Reset Auto-Tune
    #midiPort.send(mido.Message("control_change", channel = 1, control = 100, value = 127)) # On/Off Message
    osc["audioMidi"].send(mido.Message("control_change", channel = 1, control = 101, value = 0)) # Key Message
    osc["audioMidi"].send(mido.Message("control_change", channel = 1, control = 102, value = 0)) # Type Message