from PyQt6.QtWidgets import (
    QCheckBox,
    QDialog,
    QDoubleSpinBox,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QMessageBox,
    QPushButton,
    QScrollArea,
    QSlider,
    QTabWidget,
    QVBoxLayout,
    QWidget,
)
import traceback
from util.constants import VALID_IEM_MIXER_TYPES, getHeadampChannels

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

class GainDialog(QDialog):
    def __init__(self, config, widgets, osc):
        super().__init__()
        self.config = config
        self.widgets = widgets
        self.osc = osc

        vlayout = QVBoxLayout()

        if len(self.config["osc"]) == 1 or self.osc["fohClient"].mixerType not in VALID_IEM_MIXER_TYPES:
            vlayout.addWidget(self.gainTabLayer("foh")) 
        else:
            tabs = QTabWidget()
            for mixerName in self.config["osc"]:
                tabs.addTab(self.gainTabLayer(mixerName), mixerName.upper())
            vlayout.addWidget(tabs)

        self.setLayout(vlayout)

    def gainTabLayer(self, mixerName):
        try:
            headampChannels = getHeadampChannels(self.osc[mixerName + "Client"].mixerType)

            initValues = getCurrentGain(self.osc, mixerName, headampChannels)
            
            vlayout = QVBoxLayout()

            if len(headampChannels) == 1:
                for type in headampChannels:
                    vlayout.addWidget(self.gainSubTabLayer(mixerName, initValues, headampChannels, type)) 
            else:
                tabs = QTabWidget()
                for type in headampChannels:
                    tabs.addTab(self.gainSubTabLayer(mixerName, initValues, headampChannels, type), type)
                vlayout.addWidget(tabs)

            widget = QWidget()
            widget.setLayout(vlayout)
            return widget
        except Exception as ex:
            print(traceback.format_exc())
            vlayout = QVBoxLayout()
            label = QLabel("Error: " + str(ex))
            label.setStyleSheet("color:red")
            vlayout.addWidget(label)
            
            widget = QWidget()
            widget.setLayout(vlayout)
            return widget
    
    def gainSubTabLayer(self, mixerName, initValues, headampChannels, type):
        hlayout = QHBoxLayout()

        for idx, channel in enumerate(headampChannels[type]):
            vlayout = QVBoxLayout()
            label = QLabel(str(idx + 1))
            label.setFixedHeight(35)

            box = PhantomBox(self.osc, mixerName, initValues, channel)
            if self.osc[mixerName + "Client"].mixerType == "XR16":
                if idx >= 8:
                    box.setEnabled(False)
            elif self.osc[mixerName + "Client"].mixerType == "XR12":
                if idx >= 4:
                    box.setEnabled(False)

            vlayout.addWidget(label)
            vlayout.addWidget(box)
            vlayout.addWidget(GainSlider(self.osc, mixerName, initValues, channel))
            hlayout.addLayout(vlayout)

        widget = QWidget()
        widget.setLayout(hlayout)
        scroll = QScrollArea()
        scroll.setWidget(widget)
        scroll.setWidgetResizable(True)
        scroll.setMinimumHeight(450)
        return scroll

class PhantomBox(QWidget):
    def __init__(self, osc, mixerName, initValues, channel):
        super().__init__()
        self.osc = osc
        self.mixerName = mixerName
        self.command = "/headamp/" + channel + "/gain"

        layout = QHBoxLayout()

        self.box = QCheckBox()
        self.box.setChecked(initValues[self.command] == 1)
        self.box.clicked.connect(self.onClicked)

        layout.addWidget(QLabel("48V: "))
        layout.addWidget(self.box)
        self.setLayout(layout)
        self.setFixedHeight(35)
    
    def onClicked(self, checked):
        try:
            self.osc[self.mixerName + "Client"].send_message(self.command, 1 if checked else 0)
        except Exception as ex:
            print(traceback.format_exc())
            dlg = QMessageBox(self)
            dlg.setWindowTitle("Preamp Gain")
            dlg.setText("Error: " + str(ex))
            dlg.exec()
    
    def setEnabled(self, enable):
        self.box.setEnabled(enable)

class GainSlider(QWidget):
    MIN = -12.0
    MAX = 60.0
    STEP = 0.5

    def __init__(self, osc, mixerName, initValues, channel):
        super().__init__()
        self.osc = osc
        self.mixerName = mixerName
        self.command = "/headamp/" + channel + "/gain"

        layout = QGridLayout()

        self.slider = QSlider()

        self.slider.setRange(0, (self.MAX - self.MIN) / self.STEP)
        self.slider.setSingleStep(1)
        self.slider.setTickInterval(24)
        self.slider.setTickPosition(QSlider.TickPosition.TicksLeft)
        self.slider.setValue(round(initValues[self.command] * (self.MAX - self.MIN) * self.STEP))
        self.slider.valueChanged.connect(self.onSliderValueChange)
        self.slider.setMinimumWidth(20)

        self.box = QDoubleSpinBox()
        self.box.setRange(self.MIN, self.MAX)
        self.box.setSingleStep(self.STEP)
        self.box.setValue(round((initValues[self.command] * (self.MAX - self.MIN)) + self.MIN))
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
    
    def onSliderValueChange(self, value):
        self.box.setValue((value * self.STEP) + self.MIN)
    
    def onBoxValueChange(self, value):
        try:
            self.osc[self.mixerName + "Client"].send_message(self.command, (value - self.MIN) / (self.MAX - self.MIN))
            self.slider.setValue(round((value - self.MIN) / self.STEP))
        except Exception as ex:
            print(traceback.format_exc())
            dlg = QMessageBox(self)
            dlg.setWindowTitle("Preamp Gain")
            dlg.setText("Error: " + str(ex))
            dlg.exec()

def getCurrentGain(osc, mixerName, headampChannels):
    settings = {}
    for type in headampChannels:
        for channel in headampChannels[type]:
            settings["/headamp/" + channel + "/gain"] = None
            settings["/headamp/" + channel + "/phantom"] = None

    return osc[mixerName + "Client"].bulk_send_messages(settings)