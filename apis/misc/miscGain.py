import logging
from PyQt6.QtWidgets import (
    QCheckBox,
    QComboBox,
    QDialog,
    QDoubleSpinBox,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QSlider,
    QTabWidget,
    QVBoxLayout,
    QWidget,
)
import pyqtgraph
import traceback
from util.constants import ALL_CHANNELS, AUX_CHANNELS, HEADAMP_CHANNELS

logger = logging.getLogger(__name__)

class GainButton(QPushButton):
    def __init__(self, config, widgets, osc):
        super().__init__("Preamp Gain Control")
        self.config = config
        self.widgets = widgets
        self.osc = osc
        self.pressed.connect(self.clicked)
    
    def clicked(self):
        GainDialog(self.config, self.widgets, self.osc).exec()
        self.setDown(False)
        
        # Lastly, remove subscriptions
        for mixerName in self.config["osc"]:
            self.osc[mixerName + "Server"].subscription.remove("/meters/0")

class GainDialog(QDialog):
    def __init__(self, config, widgets, osc):
        super().__init__()
        self.config = config
        self.widgets = widgets
        self.osc = osc

        vlayout = QVBoxLayout()

        if len(self.config["osc"]) == 1:
            for mixerName in self.config["osc"]:
                vlayout.addWidget(self.gainTabLayer(mixerName)) 
        else:
            tabs = QTabWidget()
            for mixerName in self.config["osc"]:
                tabs.addTab(self.gainTabLayer(mixerName), mixerName.upper())
            vlayout.addWidget(tabs)

        self.setLayout(vlayout)

    def gainTabLayer(self, mixerName):
        try:            
            hlayout = QHBoxLayout()

            self.plot = MeterPlot(self.osc, mixerName)

            vlayout = QVBoxLayout()
            vlayout.addWidget(self.plot.channel)
            vlayout.addWidget(self.plot.label)
            vlayout.addWidget(self.plot.phantom)
            vlayout.addWidget(self.plot.fader)
            hWidget = QWidget()
            hWidget.setLayout(vlayout)
            hWidget.setFixedWidth(120)
            hlayout.addWidget(hWidget)

            hlayout.addWidget(self.plot)

            widget = QWidget()
            widget.setLayout(hlayout)
            return widget
        except Exception as ex:
            logger.error(traceback.format_exc())
            vlayout = QVBoxLayout()
            label = QLabel("Error: " + str(ex))
            label.setStyleSheet("color:red")
            vlayout.addWidget(label)
            
            widget = QWidget()
            widget.setLayout(vlayout)
            return widget

class MeterPlot(pyqtgraph.PlotWidget):
    def __init__(self, osc, mixerName):
        super().__init__()
        self.osc = osc
        self.mixerName = mixerName

        self.x = []
        self.y = []

        self.setBackground('w')
        self.plotLine = self.plot(self.x, self.y, pen=pyqtgraph.mkPen(color=(255, 0, 0)))
        self.osc[mixerName + "Server"].subscription.add("/meters/0", self.processSubscription)

        self.label = QLineEdit()
        self.label.setEnabled(False)

        self.channel = QComboBox()
        channels = list(set(ALL_CHANNELS) - set(AUX_CHANNELS))
        channels.sort()
        for ch in channels:
            self.channel.addItem("Ch " + "".join(ch.split("/ch/")))

        self.phantom = PhantomBox(osc, mixerName)
        self.fader = GainSlider(osc, mixerName)
        
        self.channel.setCurrentIndex(-1)
        self.channel.currentIndexChanged.connect(self.onIndexChange)
        self.channel.setCurrentIndex(0)
        
    def processSubscription(self, mixerName, message, *args):
        # TODO: Change this
        print(str(message) + ": " + str(args))
    
    def onIndexChange(self, idx):
        self.x = []
        self.y = []
        self.plotLine.setData(self.x, self.y)

        settings = {}
        settings["/‐ha/" + "{:02d}".format(idx) + "/index"] = None
        settings["/ch/" + "{:02d}".format(idx + 1) + "/config/name"] = None
        values = self.osc[self.mixerName + "Client"].bulk_send_messages(settings)
        preampChannel = values["/‐ha/" + "{:02d}".format(idx) + "/index"]

        if preampChannel == -1:
            self.phantom.disable()
            self.fader.disable()
        else:
            self.phantom.enable(preampChannel)
            self.fader.enable(preampChannel)
        
        self.label.setText(settings["/ch/" + "{:02d}".format(idx + 1) + "/config/name"])

class PhantomBox(QWidget):
    def __init__(self, osc, mixerName):
        super().__init__()
        self.osc = osc
        self.mixerName = mixerName
        self.channel = None
        self.init = False

        layout = QHBoxLayout()

        self.box = QCheckBox()
        self.box.clicked.connect(self.onClicked)

        layout.addWidget(QLabel("48V: "))
        layout.addWidget(self.box)
        self.setLayout(layout)
        self.setFixedHeight(35)

    def enable(self, channel):
        self.init = True
        self.channel = channel

        settings = {}
        settings[self.getCommand()] = None
        values = self.osc[self.mixerName + "Client"].bulk_send_messages(settings)
        value = values[self.getCommand()]

        self.box.setEnabled(True)
        self.box.setChecked(value == 1)

        self.init = False

    def disable(self):
        self.init = True
        self.channel = None

        self.box.setEnabled(False)
        self.box.setChecked(False)

        self.init = False
    
    def onClicked(self, checked):
        try:
            self.osc[self.mixerName + "Client"].send_message(self.getCommand(), 1 if checked else 0)
        except Exception as ex:
            logger.error(traceback.format_exc())
            dlg = QMessageBox(self)
            dlg.setWindowTitle("Preamp Gain")
            dlg.setText("Error: " + str(ex))
            dlg.exec()
    
    def getCommand(self):
        return "/headamp/" + "{:03d}".format(int(self.channel)) + "/phantom"

class GainSlider(QWidget):
    MIN = -12.0
    MAX = 60.0
    STEP = 0.5

    def __init__(self, osc, mixerName):
        super().__init__()
        self.osc = osc
        self.mixerName = mixerName
        self.channel = None
        self.init = False

        layout = QGridLayout()

        self.slider = QSlider()

        self.slider.setRange(0, round((self.MAX - self.MIN) / self.STEP))
        self.slider.setSingleStep(1)
        self.slider.setTickInterval(24)
        self.slider.setTickPosition(QSlider.TickPosition.TicksLeft)
        self.slider.valueChanged.connect(self.onSliderValueChange)
        self.slider.setMinimumWidth(20)

        self.box = QDoubleSpinBox()
        self.box.setRange(self.MIN, self.MAX)
        self.box.setSingleStep(self.STEP)
        self.box.valueChanged.connect(self.onBoxValueChange)

        layout.addWidget(QLabel("60.0"), 0, 0, 1, 1)
        layout.addWidget(QLabel("48.0"), 2, 0, 1, 1)
        layout.addWidget(QLabel("36.0"), 4, 0, 1, 1)
        layout.addWidget(QLabel("24.0"), 6, 0, 1, 1)
        layout.addWidget(QLabel("12.0"), 8, 0, 1, 1)
        layout.addWidget(QLabel("0.0"), 10, 0, 1, 1)
        layout.addWidget(QLabel("-12.0"), 12, 0, 1, 1)
        layout.addWidget(self.slider, 0, 1, 13, 1)
        layout.addWidget(self.box, 13, 0, 1, 2)
        
        self.setMinimumHeight(300)
        self.setLayout(layout)
    
    def enable(self, channel):
        self.init = True
        self.channel = channel

        settings = {}
        settings[self.getCommand()] = None
        values = self.osc[self.mixerName + "Client"].bulk_send_messages(settings)
        value = values[self.getCommand()]

        self.slider.setEnabled(True)
        self.slider.setValue(round(value * ((self.MAX - self.MIN) / self.STEP)))
        self.box.setEnabled(True)
        self.box.setValue(round((value * (self.MAX - self.MIN)) + self.MIN))
        self.init = False

    def disable(self):
        self.init = True
        self.channel = None

        self.slider.setEnabled(False)
        self.slider.setValue(0)
        self.box.setEnabled(False)
        self.box.setValue(0)

        self.init = False
    
    def onSliderValueChange(self, value):
        if not self.init:
            self.box.setValue((value * self.STEP) + self.MIN)
    
    def onBoxValueChange(self, value):
        if not self.init:
            try:
                self.osc[self.mixerName + "Client"].send_message(self.getCommand(), (value - self.MIN) / (self.MAX - self.MIN))
                self.slider.setValue(round((value - self.MIN) / self.STEP))
            except Exception as ex:
                logger.error(traceback.format_exc())
                dlg = QMessageBox(self)
                dlg.setWindowTitle("Preamp Gain")
                dlg.setText("Error: " + str(ex))
                dlg.exec()
    
    def getCommand(self):
        return "/headamp/" + "{:03d}".format(int(self.channel)) + "/gain"

def getCurrentGain(osc, mixerName):
    settings = {}
    for type in HEADAMP_CHANNELS:
        for channel in HEADAMP_CHANNELS[type]:
            settings["/headamp/" + channel + "/gain"] = None
            settings["/headamp/" + channel + "/phantom"] = None

    return osc[mixerName + "Client"].bulk_send_messages(settings)