import mido
from PyQt6.QtWidgets import (
    QPushButton,
)
import traceback
from util.customWidgets import ProgressDialog

class ResetButton(QPushButton):
    def __init__(self, config, osc):
        super().__init__("Yes!")
        self.config = config
        self.osc = osc
        self.pressed.connect(self.clicked)
    
    def clicked(self):
        dlg = ProgressDialog("Mute, Pan, Fader settings reset", self.main)
        dlg.exec()

        self.setDown(False)

    def main(self, dlg):
        try:
            dlg.initBar.emit(len(self.config["resetCommands"]))

            self.osc["fohClient"].bulk_send_messages(self.config["resetCommands"], dlg)

            # Reset Auto-Tune
            #self.osc["audioMidi"].send(mido.Message("control_change", channel = 1, control = 100, value = 127)) # On/Off Message
            self.osc["audioMidi"].send(mido.Message("control_change", channel = 1, control = 101, value = 0)) # Key Message
            self.osc["audioMidi"].send(mido.Message("control_change", channel = 1, control = 102, value = 0)) # Type Message
            
            print("Settings Reset")
            dlg.complete.emit()
        except Exception as ex:
            print(traceback.format_exc())
            dlg.raiseException.emit(ex)