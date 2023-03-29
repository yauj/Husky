from apis.pages.pagesMutes import MutesBox, getCurrentMutes
import logging
import math
from PyQt6.QtWidgets import (
    QCheckBox,
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
from pythonosc.udp_client import SimpleUDPClient
import struct
import threading
from util.constants import ALL_BUSES, ALL_CHANNELS, AUTOMIX_METERS_CMD, AUTOMIX_METERS_EXPECTED_FLOATS, AUX_CHANNELS, PORT
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
        if "luckyAutoMix" in self.config and "bus" in self.config["luckyAutoMix"]:
            self.bus.setCurrentText(self.config["luckyAutoMix"]["bus"])
        else:
            self.bus.setCurrentIndex(0)

        self.meter = QCheckBox()
        if "luckyAutoMix" in self.config and "postFader" in self.config["luckyAutoMix"]:
            self.meter.setChecked(self.config["luckyAutoMix"]["postFader"])

        self.min = QSpinBox()
        self.min.setRange(-120, 0)
        if "luckyAutoMix" in self.config and "min" in self.config["luckyAutoMix"]:
            self.min.setValue(self.config["luckyAutoMix"]["min"])
        else:
            self.min.setValue(-120) # Default to min

        self.threshold = QSpinBox()
        self.threshold.setRange(-120, 0)
        if "luckyAutoMix" in self.config and "threshold" in self.config["luckyAutoMix"]:
            self.threshold.setValue(self.config["luckyAutoMix"]["threshold"])
        else:
            self.threshold.setValue(-120) # Default to min

        self.mBox = QSpinBox()
        self.mBox.setRange(1, 9)
        if "luckyAutoMix" in self.config and "m" in self.config["luckyAutoMix"]:
            self.mBox.setValue(self.config["luckyAutoMix"]["m"])
        else:
            self.mBox.setValue(3)
        
        self.cBox = QSpinBox()
        self.cBox.setRange(-24, 0)
        if "luckyAutoMix" in self.config and "c" in self.config["luckyAutoMix"]:
            self.cBox.setValue(self.config["luckyAutoMix"]["c"])
        else:
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
        hlayout.addWidget(QLabel("Meter Post-Fader:"))
        hlayout.addWidget(self.meter)
        self.vlayout.addLayout(hlayout)

        hlayout = QHBoxLayout()
        hlayout.addWidget(QLabel("Min dB:"))
        hlayout.addWidget(self.min)
        hlayout.addWidget(QLabel("Threshold dB:"))
        hlayout.addWidget(self.threshold)
        self.vlayout.addLayout(hlayout)

        hlayout = QHBoxLayout()
        hlayout.addWidget(QLabel("M:"))
        hlayout.addWidget(self.mBox)
        hlayout.addWidget(QLabel("C:"))
        hlayout.addWidget(self.cBox)
        self.vlayout.addLayout(hlayout)

        for autoMixName in ["A", "B", "C", "D", "E"]:
            self.autoMixers[autoMixName] = LuckyGroup(self.config, self.osc, self.bus, self.weights, self.mutes, self.gain, self.meter, self.min, self.threshold, self.mBox, self.cBox, autoMixName)
        
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

            if "luckyAutoMix" in self.config and "mappings" in self.config["luckyAutoMix"] and channel in self.config["luckyAutoMix"]["mappings"]:
                assignment.setCurrentText(self.config["luckyAutoMix"]["mappings"][channel]["assignment"])
                weight.setValue(self.config["luckyAutoMix"]["mappings"][channel]["weight"])

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
            db = 20 * math.log10(meterVals[channelIdx + 2])
            self.gain[channelIdx].append(db)
            if len(self.gain[channelIdx]) > 3: # Keep under 3
                self.gain[channelIdx] = self.gain[channelIdx][1:]
        
    def notConnected(self):
        label = QLabel("Not connected to FOH Mixer")
        label.setStyleSheet("color:red")
        self.vlayout.addWidget(label)
    
    def closeEvent(self, a0):
        if hasattr(self, 'bus'):
            if self.bus.currentIndex() > 0:
                self.config["luckyAutoMix"] = {
                    "bus": self.bus.currentText(),
                    "postFader": self.meter.isChecked(),
                    "min": self.min.value(),
                    "threshold": self.threshold.value(),
                    "m": self.mBox.value(),
                    "c": self.cBox.value(),
                    "mappings": {}
                }
                for idx, channel in enumerate(self.assignments):
                    self.config["luckyAutoMix"]["mappings"][channel] = {
                        "assignment": self.assignments[channel].currentText(),
                        "weight": self.weights[idx].value()
                    }

            self.osc["fohServer"].subscription.remove(MUTE_SUB)
            self.osc["fohServer"].subscription.remove(AUTOMIX_METERS_CMD)
            for autoMixName in self.autoMixers:
                self.autoMixers[autoMixName].removeAll()

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
    def __init__(self, config, osc, bus, weights, mutes, gain, meter, min, threshold, mBox, cBox, name):
        self.config = config
        self.osc = osc
        self.bus = bus
        self.weights = weights
        self.mutes = mutes
        self.gain = gain
        self.meter = meter
        self.min = min
        self.threshold = threshold
        self.mBox = mBox
        self.cBox = cBox
        self.name = name

        self.lock = OwnerLock()
        self.fadersPos = {}
    
    def addChannel(self, channelIdx):
        faderCommand = "/ch/" + "{:02d}".format(channelIdx + 1) + "/mix/fader"

        self.fadersPos[channelIdx] = []
        self.osc["fohServer"].subscription.add(faderCommand, self.processSubscription, FADER_SUB_PREFIX + self.name + "/" + str(channelIdx))
    
    def removeChannel(self, channelIdx):
        self.osc["fohServer"].subscription.remove(FADER_SUB_PREFIX + self.name + "/" + str(channelIdx))

        # Reset to Unity
        command = "/ch/" + "{:02d}".format(channelIdx + 1) + "/mix/" + self.bus.currentText() + "/level"
        self.osc["fohClient"].send_message(command, 0.75)

        del self.fadersPos[channelIdx]
    
    def removeAll(self):
        faderPosCopy = self.fadersPos.copy()
        for channelIdx in faderPosCopy:
            self.removeChannel(channelIdx)

    def processSubscription(self, mixerName, message, arg):
        thisChannel = int(message.replace(FADER_SUB_PREFIX + self.name + "/", ""))
        faderVals = struct.unpack("<hhf", arg)
        self.fadersPos[thisChannel].append(faderVals[-1])

        holder = ProcessHolder(thisChannel, self.bus, self.gain, self.fadersPos)

        if holder.shouldFire:
            threads = []
            for channelIdx in holder.fadersMap:
                th = threading.Thread(target = self.calcMeterVal, args = (holder, channelIdx))
                th.start()
                threads.append(th)
            
            for th in threads:
                th.join()

            holder.calcMaxVal()

        if holder.shouldFire: # Passed all conditions
            id = str(uuid4())
            if self.lock.acquire(id):
                try:
                    m = self.mBox.value()
                    c = self.cBox.value()
                    if holder.maxChVal < self.threshold.value(): # Below Threshold, so should semi-gate all channels
                        holder.maxChVal = self.threshold.value()
                        c = 0

                    threads = []
                    for channelIdx in holder.fadersMap:
                        th = threading.Thread(target = self.fireCommand, args = (mixerName, holder, channelIdx, m, c))
                        th.start()
                        threads.append(th)
                    
                    for th in threads:
                        th.join()
                finally:
                    self.lock.release()
    
    def calcMeterVal(self, holder, channelIdx):
        if not self.mutes[channelIdx].isChecked():
            if len(holder.valsMap[channelIdx]) < 3: # Should wait for all to have multiple datapoints
                holder.shouldFire = False
            else:
                val = max(holder.valsMap[channelIdx])
                val = val + self.weights[channelIdx].value()

                if self.meter.isChecked():
                    faderPos = max(holder.fadersMap[channelIdx])
                    if faderPos >= 0.5:
                        val = val + (40 * faderPos) - 30
                    elif faderPos >= 0.25:
                        val = val + (80 * faderPos) - 50
                    elif faderPos >= 0.125:
                        val = val + (160 * faderPos) - 70
                    else:
                        val = val + (320 * faderPos) - 90

                holder.vals[channelIdx] = val
        
        if len(self.fadersPos[channelIdx]) >= 3:
            self.fadersPos[channelIdx] = self.fadersPos[channelIdx][1:] # Remove first element, to keep list small

    def fireCommand(self, mixerName, holder, channelIdx, m, c):
        fireValue = 0.25

        command = "/ch/" + "{:02d}".format(channelIdx + 1) + "/mix/" + holder.busName + "/level"
        if channelIdx in holder.vals:
            if holder.vals[channelIdx] <= self.min.value():
                fireValue = 0.25
            elif holder.vals[channelIdx] == holder.maxChVal:
                fireValue = 0.75
            else:
                fireValue = 0.5 + (math.atan((holder.vals[channelIdx] - holder.maxChVal - c) / m) / 6)
        else:
            fireValue = 0.25

        client = SimpleUDPClient(self.osc[mixerName + "Client"].ipAddress, PORT)
        client.send_message(command, fireValue)

class ProcessHolder:
    def __init__(self, thisChannel, bus, gain, fadersPos):
        # Condition that this is the first channel
        self.shouldFire = next(iter(fadersPos.keys())) == thisChannel
        # Condition that the bus is specified
        if self.shouldFire: 
            self.busName = bus.currentText()
            if self.busName == "None":
                self.shouldFire = False

        self.valsMap = gain.copy()
        self.fadersMap = fadersPos.copy()
        self.vals = {}

    def calcMaxVal(self):
        self.maxChVal = max(self.vals.values()) if len(self.vals) > 0 else None

        if self.maxChVal is None:
            self.shouldFire = False