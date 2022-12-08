import sys
import traceback
sys.path.insert(0, '../')

from PyQt6.QtWidgets import (
    QSlider,
)

class FadersSlider(QSlider):
    def __init__(self, osc, fader, index):
        super().__init__()

        self.osc = osc
        self.fader = fader
        self.index = index

        self.setRange(0, 127)
        self.setValue(0)
        self.setSingleStep(1)
        self.setTickInterval(21)
        self.setTickPosition(QSlider.TickPosition.TicksRight)
        self.valueChanged.connect(self.slider)

        self.osc["serverMidi"].callback(self.callbackFunction)

    def slider(self):
        try:
            main(self.osc, self.fader["commands"], self)
        except Exception:
            # Fail Quietly
            print(traceback.format_exc())

    def callbackFunction(self, message):
        if message.channel == 4 and message.control == 13 + self.index:
            self.setValue(message.value)

def main(osc, commands, slider):
    # Command should be in following format:
    # [foh|iem] [osc command] [min float] [max float]
    for command in commands:
        components = command.split()
        faderPosition = float(slider.value()) / 127.0
        min = float(components[2])
        max = float(components[3])
        arg = (faderPosition * (max - min)) + min
        
        if components[0] == "foh":
            osc["fohClient"].send_message(components[1], arg)
        elif components[0] == "iem":
            osc["iemClient"].send_message(components[1], arg)