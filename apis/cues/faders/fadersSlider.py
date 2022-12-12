import mido
from PyQt6.QtWidgets import (
    QSlider,
)
from time import time
import traceback

class FadersSlider(QSlider):
    def __init__(self, osc, fader, index, defaultValue, oscFeedback):
        super().__init__()

        self.osc = osc
        self.fader = fader
        self.index = index
        self.lastMidiTime = None
        self.oscFeedback = oscFeedback # MIDI knob on X32 is controlled through OSC, not MIDI

        self.setRange(0, 127)
        self.setValue(0)
        self.setSingleStep(1)
        self.setTickInterval(21)
        self.setTickPosition(QSlider.TickPosition.TicksRight)
        self.valueChanged.connect(self.slider)

        # Create Subscription if OSC command
        if len(self.fader["commands"]) > 0:
            components = self.fader["commands"][0].split()
            if components[0] == "foh":
                self.osc["fohServer"].subscription.add(components[1], self.processSubscription)
            elif components[0] == "iem":
                self.osc["iemServer"].subscription.add(components[1], self.processSubscription)

        # Set Default Value if specified
        if defaultValue:
            self.setValue(defaultValue)

        self.osc["serverMidi"].callback(self.midiInput)

    def slider(self, value):
        try:
            midiCmd = False if self.lastMidiTime is None else time() - self.lastMidiTime < 0.15

            # THIS IS HARDCODED
            if not midiCmd and self.oscFeedback is not None and self.osc["serverMidi"].input is not None:
                self.osc["fohClient"].send_message(self.oscFeedback, value)

            main(self.osc, self.fader["commands"], value, not self.isSliderDown() and not midiCmd)
        except Exception:
            # Fail Quietly
            print(traceback.format_exc())

    def midiInput(self, message):
        if message.channel == 4 and message.control == 13 + self.index:
            self.lastMidiTime = time()
            self.setValue(message.value)
    
    def processSubscription(self, arg):
        components = self.fader["commands"][0].split()
        min = float(components[2])
        max = float(components[3])
        increasingFader = max >= min
        if (increasingFader and arg > max) or (not increasingFader and arg < max):
            self.fader["commands"][0] = components[0] + " " + components[1] + " " + components[2] + " " + str(arg)
            max = arg
        elif (increasingFader and arg < min) or (not increasingFader and arg > min):
            self.fader["commands"][0] = components[0] + " " + components[1] + " " + str(arg) + " " + components[3]
            min = arg
        
        self.setValue(((arg - min) / (max - min)) * 127.0)
    
    def refreshSubscription(self, oldCommand, newCommand):
        oldComponents = oldCommand.split()
        newComponents = newCommand.split()
        
        if oldComponents[0] != newComponents[0] or oldComponents[1] != newComponents[1]:
            if oldComponents[0] == "foh":
                self.osc["fohServer"].subscription.remove(oldComponents[1])
            elif oldComponents[0] == "iem":
                self.osc["iemServer"].subscription.remove(oldComponents[1])

            if newComponents[0] == "foh":
                self.osc["fohServer"].subscription.add(newComponents[1], self.processSubscription)
            elif newComponents[0] == "iem":
                self.osc["iemServer"].subscription.add(newComponents[1], self.processSubscription)

def main(osc, commands, value, skipFirstLine):
    # Command should be in following format:
    # [foh|iem] [osc command] [min float] [max float]
    # OR
    # midi audio [channel] [control]
    #   (Fader only makes sense for control change commands)
    for idx, command in enumerate(commands):
        if idx != 0 or not skipFirstLine:
            components = command.split()
            if components[0] == "midi":
                osc[components[1] + "Midi"].send(mido.Message("control_change", channel = int(components[2]) - 1, control = int(components[3]), value = value))
            else:
                faderPosition = float(value) / 127.0
                min = float(components[2])
                max = float(components[3])
                arg = (faderPosition * (max - min)) + min
                
                if components[0] == "foh":
                    osc["fohClient"].send_message(components[1], arg)
                elif components[0] == "iem":
                    osc["iemClient"].send_message(components[1], arg)