import logging
import mido
from PyQt6.QtWidgets import (
    QSlider,
)
import traceback
from util.lock import OwnerLock

logger = logging.getLogger(__name__)

class FadersSlider(QSlider):
    def __init__(self, config, osc, fader, page, pageIdx, index, defaultValue, oscFeedback):
        super().__init__()

        self.config = config
        self.osc = osc
        self.fader = fader
        self.page = page
        self.pageIdx = pageIdx
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

    def processSubscription(self, mixerName, message, arg):
        idx, components = self.getLineComponents(mixerName, message)

        if components is None:
            return

        min = float(components[2])
        max = float(components[3])
        margin = abs(max - min) / 127.0
        increasingFader = max >= min

        midiVal = 0
        if (arg == float("inf") and increasingFader) or (arg == float("-inf") and not increasingFader):
            midiVal = 127
        elif (arg == float("-inf") and increasingFader) or (arg == float("inf") and not increasingFader):
            midiVal = 0
        else:
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
                if oldComponents[0] in ["foh", "iem"] or oldComponents[0] in self.config["osc"]:
                    self.osc[oldComponents[0] + "Server"].subscription.remove(oldComponents[1])

        for newCommand in newCommands:
            newComponents = newCommand.split()
            
            containsCommand = False
            for oldCommand in oldCommands:
                oldComponents = oldCommand.split()
                if oldComponents[0] == newComponents[0] and oldComponents[1] == newComponents[1]:
                    containsCommand = True

            if not containsCommand:
                if newComponents[0] in ["foh", "iem"] or newComponents[0] in self.config["osc"]:
                    self.osc[newComponents[0] + "Server"].subscription.add(newComponents[1], self.processSubscription)

    def onValueChange(self, value):
        try:
            # Change Target Value
            for command in self.fader["commands"]:
                components = command.split()
                if self.lock.owner != components[0] + " " + components[1]: # Don't loopback if command is source of input
                    if components[0] == "midi" and components[1] in self.config["midi"]:
                        if self.config["midi"][components[1]]["type"] == "cc":
                            self.osc[components[1] + "Midi"].send(mido.Message("control_change", channel = int(components[2]) - 1, control = int(components[3]), value = value))
                    else:
                        faderPosition = float(value) / 127.0
                        min = float(components[2])
                        max = float(components[3])
                        arg = (faderPosition * (max - min)) + min

                        if components[0] in ["foh", "iem", "atem"] or components[0] in self.config["osc"]:
                            self.osc[components[0] + "Client"].send_message(components[1], arg)
            
            # MIDI Feedback
            components = self.lock.owner.split()
            ogId = None
            if len(components) >= 2:
                if components[0] == "midi":
                    ogId = components[1]
            for portName in self.osc["serverMidi"]:
                self.osc["serverMidi"][portName].processFeedback(self.page, str(self.pageIdx + 1), value, ogId)

            # Change X32 User Encoder MIDI Knob
            if self.oscFeedback is not None:
                if len(components) >= 3 and (components[0] == "midi" and components[2] == "X-USB"):
                    return
                else:
                    self.osc["fohClient"].send_message(self.oscFeedback, value)
        except Exception:
            # Fail Quietly
            logger.error(traceback.format_exc())