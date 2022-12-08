import mido
from PyQt6.QtWidgets import (
    QSlider,
)
import traceback

class FadersSlider(QSlider):
    def __init__(self, osc, fader, index, defaultValue):
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

        if defaultValue:
            self.setValue(defaultValue)

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
    # OR
    # midi audio [channel] [control]
    #   (Fader only makes sense for control change commands)
    for command in commands:
        components = command.split()
        if components[0] == "midi":
            osc[components[1] + "Midi"].send(mido.Message("control_change", channel = int(components[2]) - 1, control = int(components[3]), value = slider.value()))
        else:
            faderPosition = float(slider.value()) / 127.0
            min = float(components[2])
            max = float(components[3])
            arg = (faderPosition * (max - min)) + min
            
            if components[0] == "foh":
                osc["fohClient"].send_message(components[1], arg)
            elif components[0] == "iem":
                osc["iemClient"].send_message(components[1], arg)