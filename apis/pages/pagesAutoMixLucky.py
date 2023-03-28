from apis.pages.pagesMutes import MutesBox, getCurrentMutes
import logging
import math
from PyQt6.QtWidgets import (
    QComboBox,
    QDoubleSpinBox,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QPushButton,
    QScrollArea,
    QSpinBox,
    QVBoxLayout,
    QWidget,
)
import struct
from util.constants import ALL_BUSES, ALL_CHANNELS, AUTOMIX_METERS_CMD, AUTOMIX_METERS_EXPECTED_FLOATS, AUX_CHANNELS
from util.lock import OwnerLock
from uuid import uuid4

logger = logging.getLogger(__name__)

FADER_SUB_PREFIX = "/lucky/fader/"
MUTE_SUB = "/lucky/mutes"

# TODO: Change Hardcode on FOH mixer
class AutoMixLuckyButton(QPushButton):
    def __init__(self, config, widgets, osc):
        super().__init__("Auto Mixer - I'm Feeling Lucky!")
        self.config = config
        self.widgets = widgets
        self.osc = osc

        self.pressed.connect(self.clicked)
    
    def clicked(self):
        if "AutoMixLucky" not in self.widgets["windows"]:
            self.widgets["windows"]["AutoMixLucky"] = AutoMixLuckyWindow(self.config, self.widgets, self.osc)
        
        self.widgets["windows"]["AutoMixLucky"].show()

        self.setDown(False)

class AutoMixLuckyWindow(QMainWindow):
    def __init__(self, config, widgets, osc):
        super().__init__()
        self.config = config
        self.widgets = widgets
        self.osc = osc
        self.autoMixers = {}
        self.assignments = {}
        self.weights = {}
        self.mutes = []
        self.gain = []

        self.vlayout = QVBoxLayout()

        if self.osc["fohClient"].connected:
            self.connected()
        else:
            self.notConnected()

        widget = QWidget()
        widget.setLayout(self.vlayout)
        self.setCentralWidget(widget)

    def connected(self):
        muteValues = getCurrentMutes(self.osc, "foh")

        self.bus = QComboBox()
        self.bus.addItem("None")
        self.bus.addItems(ALL_BUSES)
        if "luckyAutoMixBus" in self.config:
            self.bus.setCurrentText(self.config["luckyAutoMixBus"])
        else:
            self.bus.setCurrentIndex(0)

        self.threshold = QSpinBox()
        self.threshold.setRange(-80, 0)
        self.threshold.setValue(-60) # Default to -60 db

        self.mBox = QSpinBox()
        self.mBox.setRange(1, 9)
        self.mBox.setValue(3)
        
        self.cBox = QSpinBox()
        self.cBox.setRange(-24, 0)
        self.cBox.setValue(-12)

        self.vlayout.addWidget(QLabel(
            "Let Go and Let Dog. Automixes channels using specified bus.\n"
            + "This will only work if:\n"
            + "- Bus is set to Post-Fader\n"
            + "- Output to mains comes from the Bus and not the individual channels."
        ))

        hlayout = QHBoxLayout()
        hlayout.addWidget(QLabel("Bus:"))
        hlayout.addWidget(self.bus)
        self.vlayout.addLayout(hlayout)

        hlayout = QHBoxLayout()
        hlayout.addWidget(QLabel("Meter:"))
        self.meter = QComboBox()
        self.meter.addItems(["Pre-Fader", "Post-Fader"])
        self.meter.setCurrentIndex(0)
        hlayout.addWidget(self.meter)
        self.vlayout.addLayout(hlayout)

        hlayout = QHBoxLayout()
        hlayout.addWidget(QLabel("Threshold:"))
        hlayout.addWidget(self.threshold)
        hlayout.addWidget(QLabel("M:"))
        hlayout.addWidget(self.mBox)
        hlayout.addWidget(QLabel("C:"))
        hlayout.addWidget(self.cBox)
        self.vlayout.addLayout(hlayout)

        for autoMixName in ["A", "B", "C", "D", "E"]:
            self.autoMixers[autoMixName] = LuckyGroup(self.config, self.osc, self.bus, self.weights, self.mutes, self.gain, self.meter, self.threshold, self.mBox, self.cBox, autoMixName)
        
        glayout = QGridLayout()
        glayout.addWidget(QLabel("Channel"), 0, 0)
        glayout.addWidget(QLabel("Group"), 0, 1)
        glayout.addWidget(QLabel("Weight"), 0, 2)
        glayout.addWidget(QLabel("Mute"), 0, 3)

        channels = sorted(set(ALL_CHANNELS) - set(AUX_CHANNELS))
        for idx, channel in enumerate(channels):
            assignment = LuckyAssignmentBox(self.osc, self.autoMixers, idx)
            self.assignments[channel] = assignment

            weight = QDoubleSpinBox()
            weight.setRange(-12, 12)
            weight.setSingleStep(0.5)
            weight.setValue(0)
            self.weights[idx] = weight

            muteCmd = channel + "/mix/on"
            mute = MutesBox(self.osc, "foh", muteCmd, muteValues)
            self.mutes.append(mute)
            self.gain.append([])

            glayout.addWidget(QLabel(channel), idx + 1, 0)
            glayout.addWidget(assignment, idx + 1, 1)
            glayout.addWidget(weight, idx + 1, 2)
            glayout.addWidget(mute, idx + 1, 3)

        widget = QWidget()
        widget.setLayout(glayout)
        scroll = QScrollArea()
        scroll.setWidget(widget)
        scroll.setWidgetResizable(True)
        self.vlayout.addWidget(scroll)

        self.osc["fohServer"].subscription.add("/ch/**/mix/on", self.processMuteSubscription, MUTE_SUB, 1, len(channels))
        self.osc["fohServer"].subscription.add(AUTOMIX_METERS_CMD, self.processGainSubscription)

    def processMuteSubscription(self, mixerName, message, arg):
        format = "<i" + "".join(["i" for i in range(0, len(self.mutes))])
        meterVals = struct.unpack(format, arg)
        
        for i in range(0, len(self.mutes)):
            self.mutes[i].setChecked(meterVals[i + 1] == 0)
    
    def processGainSubscription(self, mixerName, message, arg):
        format = "<hh" + "".join(["f" for i in range(0, AUTOMIX_METERS_EXPECTED_FLOATS)])
        meterVals = struct.unpack(format, arg)

        for channelIdx in range(0, len(self.gain)):
            db = 20 * math.log10(max(meterVals[channelIdx + 2], 0.0001))
            self.gain[channelIdx].append(db)
            if len(self.gain[channelIdx]) > 3: # Keep under 3
                self.gain[channelIdx] = self.gain[channelIdx][1:]
        
    def notConnected(self):
        label = QLabel("Not connected to FOH Mixer")
        label.setStyleSheet("color:red")
        self.vlayout.addWidget(label)
    
    def closeEvent(self, a0):
        self.osc["fohServer"].subscription.remove(MUTE_SUB)
        self.osc["fohServer"].subscription.remove(AUTOMIX_METERS_CMD)
        for autoMixName in self.autoMixers:
            self.autoMixers[autoMixName].removeAll()
        
        if self.bus.currentIndex() > 0:
            self.config["luckyAutoMixBus"] = self.bus.currentText()

        del self.widgets["windows"]["AutoMixLucky"]

class LuckyAssignmentBox(QComboBox):
    def __init__(self, osc, autoMixers, channelIdx):
        super().__init__()
        self.osc = osc
        self.autoMixers = autoMixers
        self.channelIdx = channelIdx
        self.currentTxt = "OFF"

        self.addItem("OFF")
        for autoMixerName in self.autoMixers:
            self.addItem(autoMixerName)
        self.setCurrentText(self.currentTxt)

        self.currentTextChanged.connect(self.onTextChange)
    
    def onTextChange(self, newTxt):
        if self.currentTxt != "OFF":
            self.autoMixers[self.currentTxt].removeChannel(self.channelIdx)
        
        self.currentTxt = newTxt

        if newTxt != "OFF":
            self.autoMixers[newTxt].addChannel(self.channelIdx)

class LuckyGroup:
    MIN = -80.0

    def __init__(self, config, osc, bus, weights, mutes, gain, meter, threshold, mBox, cBox, name):
        self.config = config
        self.osc = osc
        self.bus = bus
        self.mutes = mutes
        self.weights = weights
        self.gain = gain
        self.meter = meter
        self.threshold = threshold
        self.mBox = mBox
        self.cBox = cBox
        self.name = name

        self.allOff = False

        self.lock = OwnerLock()
        self.fadersPos = {}
    
    def addChannel(self, channelIdx):
        faderCommand = "/ch/" + "{:02d}".format(channelIdx + 1) + "/mix/fader"

        self.fadersPos[channelIdx] = []
        self.osc["fohServer"].subscription.add(faderCommand, self.processSubscription, FADER_SUB_PREFIX + self.name + "/" + str(channelIdx))
        self.allOff = False
    
    def removeChannel(self, channelIdx):
        self.osc["fohServer"].subscription.remove(FADER_SUB_PREFIX + self.name + "/" + str(channelIdx))

        # Reset to Unity
        command = "/ch/" + "{:02d}".format(channelIdx + 1) + "/mix/" + self.bus.currentText() + "/level"
        self.osc["fohClient"].send_message(command, 0.75)

        del self.fadersPos[channelIdx]
    
    def removeAll(self):
        for channelIdx in self.fadersPos:
            self.removeChannel(channelIdx)

    def processSubscription(self, mixerName, message, arg):
        channelIdx = int(message.replace(FADER_SUB_PREFIX + self.name + "/", ""))
        self.fadersPos[channelIdx].append(arg)

        # Figure out if we should fire commands
        shouldFire = next(iter(self.fadersPos.keys())) == channelIdx

        if shouldFire: # Passed condition that this is the first channelIdx
            busName = self.bus.currentText()
            if busName == "None":
                shouldFire = False

        if shouldFire: # Passed condition that bus is specified
            valsMap = self.gain.copy()
            fadersMap = self.fadersPos.copy()
            vals = {}

            maxChVal = None
            for channelIdx in valsMap:
                if self.mutes[channelIdx].isChecked():
                    shouldFire = False
                else:
                    if len(fadersMap[channelIdx]) < 3: # Should wait for all to have multiple datapoints
                        shouldFire = False
                    else:
                        val = max(valsMap[channelIdx])
                        val = val + self.weights[channelIdx].value()

                        if self.meter.currentIndex() > 0:
                            faderPos = max(fadersMap[channelIdx])
                            if faderPos >= 0.5:
                                val = val + (40 * faderPos) - 30
                            elif faderPos >= 0.25:
                                val = val + (80 * faderPos) - 50
                            elif faderPos >= 0.125:
                                val = val + (160 * faderPos) - 70
                            else:
                                val = val + (320 * faderPos) - 90

                        vals[channelIdx] = val
                        if maxChVal is None or val > maxChVal:
                            maxChVal = val
        
            if shouldFire: # Pass condition that there are values for every channel
                for channelIdx in self.fadersPos:
                    self.fadersPos[channelIdx] = []

            if maxChVal is None:
                shouldFire = False
            elif maxChVal <= self.MIN and self.allOff: # It's all off already. Leave it be till there is a non-zero value
                shouldFire = False

        if shouldFire: # Passed all conditions
            id = str(uuid4())
            if self.lock.acquire(id):
                try:
                    m = self.mBox.value()
                    c = self.cBox.value()
                    if maxChVal <= self.threshold.value(): # Below Threshold, so should semi-gate all channels
                        maxChVal = self.threshold.value()
                        c = 0

                    commands = {}
                    for channelIdx in valsMap:
                        command = "/ch/" + "{:02d}".format(channelIdx + 1) + "/mix/" + busName + "/level"
                        if channelIdx in vals:
                            if vals[channelIdx] <= self.MIN:
                                commands[command] = 0.25
                            elif vals[channelIdx] == maxChVal and maxChVal > self.threshold.value():
                                commands[command] = 0.75
                            else:
                                commands[command] = 0.5 + (math.atan((vals[channelIdx] - maxChVal - m) / c) / 6)
                        else:
                            commands[command] = 0.25
                        #print(command + ": " + str(vals[channelIdx]) + "->" + str(commands[command])) TODO REMOVE
                    self.osc[mixerName + "Client"].bulk_send_messages(commands)
                finally:
                    self.lock.release()
                    self.allOff = (maxChVal <= self.MIN)