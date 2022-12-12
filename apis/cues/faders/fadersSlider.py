import mido
from PyQt6.QtWidgets import (
    QSlider,
)
import traceback
from util.lock import OwnerLock

# Command should be in following format:
# [foh|iem] [osc command] [min float] [max float]
# OR
# midi audio [channel] [control]
#   (Fader only makes sense for control change commands)
class FadersSlider(QSlider):
    def __init__(self, osc, fader, index, defaultValue, oscFeedback):
        super().__init__()

        self.osc = osc
        self.fader = fader
        self.index = index
        self.oscFeedback = oscFeedback # MIDI knob on X32 is controlled through OSC, not MIDI

        self.lock = OwnerLock()

        self.setRange(0, 127)
        self.setValue(0)
        self.setSingleStep(1)
        self.setTickInterval(21)
        self.setTickPosition(QSlider.TickPosition.TicksRight)
        self.valueChanged.connect(self.onValueChange)
        self.sliderPressed.connect(self.lock.acquireMaster)
        self.sliderReleased.connect(self.lock.release)

        self.refreshSubscription([], self.fader["commands"])

        # Set Default Value if specified
        if defaultValue:
            self.setValue(defaultValue)

        self.osc["serverMidi"].callback(self.midiInput)

    def midiInput(self, message):
        if message.channel == 4 and message.control == 13 + self.index:
            if self.lock.acquire("midi"):
                self.setValue(message.value)
    
    # TODO: What happens if a command is in multiple? Right now will just override
    def processSubscription(self, mixerName, message, arg):
        idx, components = self.getLineComponents(mixerName, message)

        if components is None:
            return

        min = float(components[2])
        max = float(components[3])
        margin = abs(max - min) / 127.0
        increasingFader = max >= min
        if (increasingFader and arg > max + margin) or (not increasingFader and arg < max - margin):
            self.fader["commands"][idx] = components[0] + " " + components[1] + " " + components[2] + " " + str(arg)
            max = arg
        elif (increasingFader and arg < min - margin) or (not increasingFader and arg > min + margin):
            self.fader["commands"][idx] = components[0] + " " + components[1] + " " + str(arg) + " " + components[3]
            min = arg
        
        midiVal = round(((arg - min) / (max - min)) * 127.0)

        if midiVal == self.value():
            return
        
        if self.lock.acquire(mixerName + " " + message):
            self.setValue(midiVal)
    
    def getLineComponents(self, mixerName, message):
        for idx, command in enumerate(self.fader["commands"]):
            components = command.split()
            if components[0] == mixerName and components[1] == message:
                return idx, components
        return None
    
    def refreshSubscription(self, oldCommands, newCommands):
        for oldCommand in oldCommands:
            oldComponents = oldCommand.split()
            
            containsCommand = False
            for newCommand in newCommands:
                newComponents = newCommand.split()
                if oldComponents[0] == newComponents[0] and oldComponents[1] == newComponents[1]:
                    containsCommand = True

            if not containsCommand:
                if oldComponents[0] == "foh":
                    self.osc["fohServer"].subscription.remove(oldComponents[1])
                elif oldComponents[0] == "iem":
                    self.osc["iemServer"].subscription.remove(oldComponents[1])

        for newCommand in newCommands:
            newComponents = newCommand.split()
            
            containsCommand = False
            for oldCommand in oldCommands:
                oldComponents = oldCommand.split()
                if oldComponents[0] == newComponents[0] and oldComponents[1] == newComponents[1]:
                    containsCommand = True

            if not containsCommand:
                if newComponents[0] == "foh":
                    self.osc["fohServer"].subscription.add(newComponents[1], self.processSubscription)
                elif newComponents[0] == "iem":
                    self.osc["iemServer"].subscription.add(newComponents[1], self.processSubscription)

    def onValueChange(self, value):
        try:
            # Change X32 Value
            for command in self.fader["commands"]:
                components = command.split()
                if self.lock.owner != components[0] + " " + components[1]: # Don't loopback if command is source of input
                    if components[0] == "midi":
                        self.osc[components[1] + "Midi"].send(mido.Message("control_change", channel = int(components[2]) - 1, control = int(components[3]), value = value))
                    else:
                        faderPosition = float(value) / 127.0
                        min = float(components[2])
                        max = float(components[3])
                        arg = (faderPosition * (max - min)) + min
                        
                        if components[0] == "foh":
                            self.osc["fohClient"].send_message(components[1], arg)
                        elif components[0] == "iem":
                            self.osc["iemClient"].send_message(components[1], arg)
            
            # Change X32 User Encoder MIDI Knob
            if self.lock.owner != "midi": # Don't loopback if MIDI is source of input
                if self.osc["serverMidi"].input is not None and self.oscFeedback is not None: # Is source of midi input and has OSC feedback command
                    self.osc["fohClient"].send_message(self.oscFeedback, value)
        except Exception:
            # Fail Quietly
            print(traceback.format_exc())