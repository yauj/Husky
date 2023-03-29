from apis.pages.pagesMutes import MutesBox
import logging
from PyQt6.QtWidgets import (
    QCheckBox,
    QComboBox,
    QDoubleSpinBox,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QWidget,
)
import struct

logger = logging.getLogger(__name__)

METER_CMD = "/meters/16"
METER_EXPECTED_COMP_VALS = 44
METER_EXPECTED_AMIX_VALS = 8

class AutoMixButton(QPushButton):
    def __init__(self, config, widgets, osc):
        super().__init__("Auto Mixer - Native")
        self.config = config
        self.widgets = widgets
        self.osc = osc
        self.pressed.connect(self.clicked)
    
    def clicked(self):
        if "AutoMix" not in self.widgets["windows"]:
            self.widgets["windows"]["AutoMix"] = AutoMixWindow(self.config, self.widgets, self.osc)
        
        self.widgets["windows"]["AutoMix"].show()

        self.setDown(False)

class AutoMixWindow(QMainWindow):
    def __init__(self, config, widgets, osc):
        super().__init__()
        self.config = config
        self.widgets = widgets
        self.osc = osc
        self.labels = {}
        self.values = {}
        self.assignments = {}
        self.mutes = {}

        self.vlayout = QVBoxLayout()

        for mixerName in self.config["osc"]:
            if self.osc[mixerName + "Client"].connected:
                self.labels[mixerName] = []
                self.values[mixerName] = []
                self.assignments[mixerName] = []
                self.mutes[mixerName] = []
                self.connected(mixerName), mixerName.upper()
            else:
                self.notConnected(mixerName), mixerName.upper()

        widget = QWidget()
        widget.setLayout(self.vlayout)
        self.setCentralWidget(widget)

    def connected(self, mixerName):
        initValues = getCurrentAutoMix(self.osc, mixerName)

        label = QLabel(mixerName.upper() + " Mixer:")
        label.setStyleSheet("font-weight: bold")
        self.vlayout.addWidget(label)

        hlayout = QHBoxLayout()
        label = QLabel("Group X enabled:")
        label.setStyleSheet("color:rgb(0, 200, 0);")
        hlayout.addWidget(label)
        hlayout.addWidget(EnabledBox(self.osc, mixerName, "X", initValues))
        label = QLabel("Group Y enabled:")
        label.setStyleSheet("color:rgb(0, 0, 200);")
        hlayout.addWidget(label)
        hlayout.addWidget(EnabledBox(self.osc, mixerName, "Y", initValues))
        self.vlayout.addLayout(hlayout)

        glayout = QGridLayout()
        glayout.addWidget(QLabel("Channel"), 0, 0)
        glayout.addWidget(QLabel("Group"), 1, 0)
        glayout.addWidget(QLabel("Weight"), 2, 0)
        glayout.addWidget(QLabel("Mute"), 3, 0)
        for channel in range(1, 9):
            label = QLabel("Ch " + str(channel))
            assignment = AssignmentBox(self.osc, mixerName, channel, initValues)
            muteCmd = "/ch/" + "{:02d}".format(channel) + "/mix/on"
            mute = MutesBox(self.osc, mixerName, muteCmd, initValues)
            glayout.addWidget(label, 0, channel)
            glayout.addWidget(assignment, 1, channel)
            glayout.addWidget(WeightBox(self.osc, mixerName, channel, initValues), 2, channel)
            glayout.addWidget(mute, 3, channel)
            self.values[mixerName].append([])
            self.labels[mixerName].append(label)
            self.assignments[mixerName].append(assignment)
            self.mutes[mixerName].append(mute)
            self.osc[mixerName + "Server"].subscription.add(muteCmd, self.processMuteSubscription)

        self.vlayout.addLayout(glayout)

        self.osc[mixerName + "Server"].subscription.add(METER_CMD, self.processMeterSubscription)
        
    def notConnected(self, mixerName):
        self.vlayout.addWidget(QLabel(mixerName.upper() + " Mixer:"))
        label = QLabel("Not connected to " + mixerName.upper() + " Mixer")
        label.setStyleSheet("color:red")
        self.vlayout.addWidget(label)

    def processMeterSubscription(self, mixerName, message, arg):
        format = "<hh" + "".join(["f" for i in range(0, METER_EXPECTED_COMP_VALS)]) + "".join(["h" for i in range(0, METER_EXPECTED_AMIX_VALS)])
        meterVals = struct.unpack(format, arg)

        for idx, val in enumerate(meterVals[-8:]):
            self.values[mixerName][idx].append(min(max(round((2 ** (val / 256)) * 255), 0), 255))
            if len(self.values[mixerName][idx]) > 10:
                values = self.values[mixerName][idx]
                self.values[mixerName][idx] = []
                if self.mutes[mixerName][idx].isChecked():
                    self.labels[mixerName][idx].setStyleSheet("color:rgb(255, 0, 0);")
                else:
                    if self.assignments[mixerName][idx].currentIndex() == 1:
                        self.labels[mixerName][idx].setStyleSheet("color:rgb(0, " + str(sum(values) / len(values)) + ", 0);")
                    elif self.assignments[mixerName][idx].currentIndex() == 2:
                        self.labels[mixerName][idx].setStyleSheet("color:rgb(0, 0, " + str(sum(values) / len(values)) + ");")
                    else:
                        self.labels[mixerName][idx].setStyleSheet("color:rgb(255, 255, 255);")
    
    def processMuteSubscription(self, mixerName, message, arg):
        idx = int(message.split("/")[2]) - 1
        if self.mutes[mixerName][idx].isChecked() != (arg == 0):
            self.mutes[mixerName][idx].setChecked(arg == 0)
    
    def closeEvent(self, a0):
        for mixerName in self.config["osc"]:
            self.osc[mixerName + "Server"].subscription.remove(METER_CMD)
            for channel in range(1, 9):
                self.osc[mixerName + "Server"].subscription.remove("/ch/" + "{:02d}".format(channel) + "/mix/on")

        del self.widgets["windows"]["AutoMix"]

class EnabledBox(QCheckBox):
    def __init__(self, osc, mixerName, group, initValues):
        super().__init__()
        self.osc = osc
        self.mixerName = mixerName
        self.command = "/config/amixenable/" + group

        self.setChecked(initValues[self.command] == 1)

        self.stateChanged.connect(self.onChange)
    
    def onChange(self, state):
        self.osc[self.mixerName + "Client"].send_message(self.command, 1 if state > 0 else 0)

class AssignmentBox(QComboBox):
    def __init__(self, osc, mixerName, channel, initValues):
        super().__init__()
        self.osc = osc
        self.mixerName = mixerName
        self.command = "/ch/" + "{:02d}".format(channel) + "/automix/group"

        self.addItems(["Off", "X", "Y"])
        self.setCurrentIndex(initValues[self.command])

        self.currentIndexChanged.connect(self.onIndexChange)
    
    def onIndexChange(self, idx):
        self.osc[self.mixerName + "Client"].send_message(self.command, idx)

class WeightBox(QDoubleSpinBox):
    MIN = -12
    MAX = 12
    STEP = 0.5

    def __init__(self, osc, mixerName, channel, initValues):
        super().__init__()
        self.osc = osc
        self.mixerName = mixerName
        self.command = "/ch/" + "{:02d}".format(channel) + "/automix/weight"

        self.setRange(self.MIN, self.MAX)
        self.setSingleStep(self.STEP)

        self.setValue((initValues[self.command] * (self.MAX - self.MIN)) + self.MIN)

        self.valueChanged.connect(self.onValueChange)
    
    def onValueChange(self, value):
        self.osc[self.mixerName + "Client"].send_message(self.command, (value - self.MIN) / (self.MAX - self.MIN))

def getCurrentAutoMix(osc, mixerName, dlg = None):
    settings = {
        "/config/amixenable/X": None,
        "/config/amixenable/Y": None
    }
    for channel in range(1, 9):
        settings["/ch/" + "{:02d}".format(channel) + "/automix/group"] = None
        settings["/ch/" + "{:02d}".format(channel) + "/automix/weight"] = None
        settings["/ch/" + "{:02d}".format(channel) + "/mix/on"] = None

    if dlg:
        dlg.initBar.emit(len(settings))

    return osc[mixerName + "Client"].bulk_send_messages(settings, dlg)