import os.path
import sys
sys.path.insert(0, '../')

from apis.snippets.loadSingle import runSingle
import asyncio
import mido
from util.constants import MIDI_BUS, KEYS
from PyQt6.QtWidgets import (
    QMessageBox,
    QPushButton,
)

class CueFireButton(QPushButton):
    def __init__(self, widgets, osc, index, options):
        super().__init__("Fire")
        if (len(index) == 1):
            super().setShortcut("ctrl+" + index)
        elif (index == "10"):
            super().setShortcut("ctrl+0")

        self.widgets = widgets
        self.osc = osc
        self.index = index
        self.options = options
        self.pressed.connect(self.clicked)
    
    def clicked(self):
        asyncio.run(main(
            self.osc,
            self.options
        ))
        
        dlg = QMessageBox(self)
        dlg.setWindowTitle("Cue")
        dlg.setText("Cue " + self.index + " Fired")
        dlg.exec()
        
async def main(osc, options):
    if options["key"].currentText() != "":
        print(mido.Backend("mido.backends.rtmidi").get_output_names())

        val = int((KEYS.index(options["key"].currentText()) * 127) / 11)
        tuneMsg = mido.Message("control_change", channel = 1, control = 100, value = 127)
        rootMsg = mido.Message("control_change", channel = 1, control = 101, value = val)
        typeMsg = mido.Message("control_change", channel = 1, control = 102, value = 127)

        midiPort = mido.Backend("mido.backends.rtmidi").open_output(MIDI_BUS)
        midiPort.send(tuneMsg)
        midiPort.send(rootMsg)
        midiPort.send(typeMsg)

    if options["lead"].currentText() != "":
        bkgdVox = ["05", "06", "07", "08"]
        leadVox = ""
        if options["lead"].currentText() == "1":
            leadVox = "05"
            bkgdVox.remove(leadVox)
        elif options["lead"].currentText() == "2":
            leadVox = "06"
            bkgdVox.remove(leadVox)
        elif options["lead"].currentText() == "3":
            leadVox = "07"
            bkgdVox.remove(leadVox)
        elif options["lead"].currentText() == "4":
            leadVox = "08"
            bkgdVox.remove(leadVox)
            
        await osc["fohClient"].send_message("/ch/" + leadVox + "/mix/01/on", 1)
        await osc["fohClient"].send_message("/ch/" + leadVox + "/mix/02/on", 1)
        await osc["fohClient"].send_message("/ch/" + leadVox + "/mix/03/on", 0)
        for ch in bkgdVox:
            await osc["fohClient"].send_message("/ch/" + ch + "/mix/01/on", 0)
            await osc["fohClient"].send_message("/ch/" + ch + "/mix/02/on", 0)
            await osc["fohClient"].send_message("/ch/" + ch + "/mix/03/on", 1)
    
    if options["snippet"].text() != "":
        if os.path.exists("data/" + options["snippet"].text()):
            await runSingle(osc, options["snippet"].text(), False)