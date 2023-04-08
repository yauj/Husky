from apis.snippets.saveSingle import appendSettingsToTextbox
import logging
from PyQt6.QtWidgets import (
    QCheckBox,
    QComboBox,
    QDialog,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QMessageBox,
    QPushButton,
    QSpinBox,
    QTabWidget,
    QVBoxLayout,
    QWidget,
)
import traceback
from util.constants import ALL_BUSES, ALL_CHANNELS, ALL_MATRICIES, AUX_CHANNELS, ODD_BUSES, ODD_MATRICIES, SETTINGS, SETTINGS_BUS_MTX

logger = logging.getLogger(__name__)

class SnippetAddButton(QPushButton):
    def __init__(self, config, osc, textbox):
        super().__init__("Add Commands")
        self.config = config
        self.osc = osc
        self.textbox = textbox
        self.pressed.connect(self.clicked)
    
    def clicked(self):
        SnippetAddDialog(self.config, self.osc, self.textbox).exec()
        self.setDown(False)

class SnippetAddDialog(QDialog):
    def __init__(self, config, osc, textbox):
        super().__init__()
        self.config = config
        self.osc = osc
        self.textbox = textbox

        layout = QVBoxLayout()
        tabs = QTabWidget()
        tabs.addTab(self.mixerPresetsLayer(), "Mixer Presets")
        tabs.addTab(self.mixerStripLayer(), "Mixer Strip")
        tabs.addTab(self.mixerSendLayer(), "Mixer Sends")
        tabs.addTab(self.midiLayer(), "MIDI")
        layout.addWidget(tabs)

        self.setLayout(layout)
    
    def mixerPresetsLayer(self):
        layout = QGridLayout()

        label = QLabel("Channel")
        label.setFixedHeight(10)
        layout.addWidget(label, 0, 1)
        label = QLabel("IEM Bus")
        label.setFixedHeight(10)
        layout.addWidget(label, 0, 2)

        boxes = {}
        for idx, name in enumerate(self.config["personal"]):
            layout.addWidget(QLabel(name + ": "), idx + 1, 0)
            boxes[name] = {}
            if "channels" in self.config["personal"][name]:
                boxes[name]["channels"] = QCheckBox()
                layout.addWidget(boxes[name]["channels"], idx + 1, 1)
            if "iem_bus" in self.config["personal"][name]:
                boxes[name]["iem_bus"] = QCheckBox()
                layout.addWidget(boxes[name]["iem_bus"], idx + 1, 2)

        layout.addWidget(AddPresetButton(self.config, self.osc, self.textbox, boxes), idx + 2, 0, 1, 3)
        
        widget = QWidget()
        widget.setLayout(layout)
        return widget


    def mixerStripLayer(self):
        vlayout = QVBoxLayout()

        hlayout = QHBoxLayout()
        hlayout.addWidget(QLabel("Mixer: "))
        mixer = QComboBox()
        for name in self.config["osc"]:
            mixer.addItem(name)
        if "foh" in self.config["osc"]:
            mixer.setCurrentText("foh")
        else:
            mixer.setCurrentIndex(0)
        hlayout.addWidget(mixer)
        vlayout.addLayout(hlayout)

        hlayout = QHBoxLayout()
        hlayout.addWidget(QLabel("Channel: "))
        self.channel = QComboBox()
        self.channel.addItems(ALL_CHANNELS)
        self.channel.addItems(["/bus/" + bus for bus in ALL_BUSES])
        self.channel.addItems(["/mtx/" + mtx for mtx in ALL_MATRICIES])
        self.channel.currentIndexChanged.connect(self.disableHPF)
        hlayout.addWidget(self.channel)
        vlayout.addLayout(hlayout)

        self.settings = {}
        for category in SETTINGS:
            hlayout = QHBoxLayout()
            hlayout.addWidget(QLabel(category + ": "))
            self.settings[category] = QCheckBox()
            hlayout.addWidget(self.settings[category])
            vlayout.addLayout(hlayout)

        hlayout = QHBoxLayout()
        hlayout.addWidget(QLabel("Fader: "))
        fader = QCheckBox()
        hlayout.addWidget(fader)
        vlayout.addLayout(hlayout)

        vlayout.addWidget(AddStripButton(self.osc, self.textbox, mixer, self.channel, self.settings, fader))

        widget = QWidget()
        widget.setLayout(vlayout)
        return widget

    def mixerSendLayer(self):
        vlayout = QVBoxLayout()

        hlayout = QHBoxLayout()
        hlayout.addWidget(QLabel("Mixer: "))
        mixer = QComboBox()
        for name in self.config["osc"]:
            mixer.addItem(name)
        if "iem" in self.config["osc"]:
            mixer.setCurrentText("iem")
        else:
            mixer.setCurrentIndex(0)
        hlayout.addWidget(mixer)
        vlayout.addLayout(hlayout)

        hlayout = QHBoxLayout()
        hlayout.addWidget(QLabel("Sends for: "))
        target = QComboBox()
        target.addItems(["/bus/" + bus for bus in ALL_BUSES])
        target.addItems(["/mtx/" + mtx for mtx in ALL_MATRICIES])
        hlayout.addWidget(target)
        vlayout.addLayout(hlayout)

        vlayout.addWidget(AddSendsButton(self.osc, self.textbox, mixer, target))

        widget = QWidget()
        widget.setLayout(vlayout)
        return widget

    def midiLayer(self):
        vlayout = QVBoxLayout()

        device = MIDIBox(self.config)

        hlayout = QHBoxLayout()
        hlayout.addWidget(QLabel("Device: "))
        hlayout.addWidget(device)
        vlayout.addLayout(hlayout)

        hlayout = QHBoxLayout()
        hlayout.addWidget(QLabel("Channel: "))
        hlayout.addWidget(device.channel)
        vlayout.addLayout(hlayout)

        hlayout = QHBoxLayout()
        hlayout.addWidget(QLabel("Control: "))
        hlayout.addWidget(device.control)
        vlayout.addLayout(hlayout)

        hlayout = QHBoxLayout()
        hlayout.addWidget(QLabel("Value: "))
        hlayout.addWidget(device.value)
        vlayout.addLayout(hlayout)

        vlayout.addWidget(AddMIDIButton(self.textbox, device, device.channel, device.control, device.value))

        widget = QWidget()
        widget.setLayout(vlayout)
        return widget
    
    # Disable HPF and Dynamics if AUX channel selected
    def disableHPF(self):
        if self.channel.currentText() in AUX_CHANNELS:
            self.settings["HPF"].setEnabled(False)
            self.settings["HPF"].setChecked(False)
            self.settings["Dynamics"].setEnabled(False)
            self.settings["Dynamics"].setChecked(False)
        elif self.channel.currentText() not in ALL_CHANNELS:
            self.settings["HPF"].setEnabled(False)
            self.settings["HPF"].setChecked(False)
            self.settings["Dynamics"].setEnabled(True)
        else:
            self.settings["HPF"].setEnabled(True)
            self.settings["Dynamics"].setEnabled(True)

class AddPresetButton(QPushButton):
    def __init__(self, config, osc, textbox, boxes):
        super().__init__("Add")
        self.config = config
        self.osc = osc
        self.textbox = textbox
        self.boxes = boxes
        self.pressed.connect(self.clicked)
    
    def clicked(self):
        try:
            self.main()

            dlg = QMessageBox(self)
            dlg.setWindowTitle("Add")
            dlg.setText("Settings Added")
            dlg.exec()
        except Exception as ex:
            logger.error(traceback.format_exc())
            dlg = QMessageBox(self)
            dlg.setWindowTitle("Add")
            dlg.setText("Error: " + str(ex))
            dlg.exec()

        self.setDown(False)
    
    def main(self):
        fohSettings = {}
        iemSettings = {}

        for name in self.boxes:
            if "channels" in self.boxes[name] and self.boxes[name]["channels"].isChecked():
                for channel in self.config["personal"][name]["channels"]:
                    for category in SETTINGS:
                        for param in SETTINGS[category]:
                            fohSettings["/ch/" + channel + param] = None

            if "iem_bus" in self.boxes[name] and self.boxes[name]["iem_bus"].isChecked():
                for channel in ALL_CHANNELS:
                    if self.config["personal"][name]["iem_bus"] == "st": # Main Stereo Out
                        iemSettings[channel + "/mix/fader"] = None
                        iemSettings[channel + "/mix/pan"] = None
                    elif self.config["personal"][name]["iem_bus"] == "mono": # Mono Out
                        iemSettings[channel + "/mix/mlevel"] = None
                    else:
                        prefix = channel + "/mix/" + self.config["personal"][name]["iem_bus"]

                        iemSettings[prefix + "/level"] = None
                        if self.config["personal"][name]["iem_bus"] in ODD_BUSES:
                            iemSettings[prefix + "/pan"] = None

        if len(fohSettings) > 0:
            appendSettingsToTextbox(self.osc, self.textbox, "foh", fohSettings)
        
        if len(iemSettings) > 0:
            appendSettingsToTextbox(self.osc, self.textbox, "iem", iemSettings)
                
                

class AddStripButton(QPushButton):
    def __init__(self, osc, textbox, mixer, channel, settings, fader):
        super().__init__("Add")
        self.osc = osc
        self.textbox = textbox
        self.mixer = mixer
        self.channel = channel
        self.settings = settings
        self.fader = fader
        self.pressed.connect(self.clicked)
    
    def clicked(self):
        try:
            self.main()
            
            dlg = QMessageBox(self)
            dlg.setWindowTitle("Add")
            dlg.setText("Settings Added")
            dlg.exec()
        except Exception as ex:
            logger.error(traceback.format_exc())
            dlg = QMessageBox(self)
            dlg.setWindowTitle("Add")
            dlg.setText("Error: " + str(ex))
            dlg.exec()

        self.setDown(False)

    def main(self):
        settings = {}
        for category in self.settings:
            if self.settings[category].isChecked():
                if "/bus/" in self.channel.currentText() or "/mtx/" in self.channel.currentText():
                    for param in SETTINGS_BUS_MTX[category]:
                        settings[self.channel.currentText() + param] = None
                else:
                    for param in SETTINGS[category]:
                        settings[self.channel.currentText() + param] = None

        if self.fader.isChecked():
            settings[self.channel.currentText() + "/mix/fader"] = None

        if len(settings) > 0:
            appendSettingsToTextbox(self.osc, self.textbox, self.mixer.currentText(), settings)

class AddSendsButton(QPushButton):
    def __init__(self, osc, textbox, mixer, target):
        super().__init__("Add")
        self.osc = osc
        self.textbox = textbox
        self.mixer = mixer
        self.target = target
        self.pressed.connect(self.clicked)
    
    def clicked(self):
        try:
            self.main()
            
            dlg = QMessageBox(self)
            dlg.setWindowTitle("Add")
            dlg.setText("Settings Added")
            dlg.exec()
        except Exception as ex:
            logger.error(traceback.format_exc())
            dlg = QMessageBox(self)
            dlg.setWindowTitle("Add")
            dlg.setText("Error: " + str(ex))
            dlg.exec()

        self.setDown(False)

    def main(self):
        settings = {}
        if "/bus/" in self.target.currentText():
            bus = self.target.currentText().split("/bus/")[1]
            for channel in ALL_CHANNELS:
                prefix = channel + "/mix/" + bus

                settings[prefix + "/on"] = None
                settings[prefix + "/level"] = None

                if bus in ODD_BUSES:
                    settings[prefix + "/pan"] = None
        else: # is /mtx/
            mtx = self.target.currentText().split("/mtx/")[1]
            for bus in ALL_BUSES:
                prefix = "/bus/" + bus + "/mix/" + mtx

                settings[prefix + "/on"] = None
                settings[prefix + "/level"] = None

                if mtx in ODD_MATRICIES:
                    settings[prefix + "/pan"] = None
        
        appendSettingsToTextbox(self.osc, self.textbox, self.mixer.currentText(), settings)

class AddMIDIButton(QPushButton):
    def __init__(self, textbox, type, channel, control, value):
        super().__init__("Add")
        self.textbox = textbox
        self.type = type
        self.channel = channel
        self.control = control
        self.value = value
        self.pressed.connect(self.clicked)
    
    def clicked(self):
        try:
            self.textbox.append("midi " + self.type.currentText() + " " + str(self.channel.value()) + " " + str(self.control.value()) + " " + str(self.value.value()))
            
            dlg = QMessageBox(self)
            dlg.setWindowTitle("Add")
            dlg.setText("Settings Added")
            dlg.exec()
        except Exception as ex:
            logger.error(traceback.format_exc())
            dlg = QMessageBox(self)
            dlg.setWindowTitle("Add")
            dlg.setText("Error: " + str(ex))
            dlg.exec()

        self.setDown(False)

class MIDIBox(QComboBox):
    def __init__(self, config):
        super().__init__()
        self.config = config

        self.channel = QSpinBox()
        self.channel.setMinimum(1)
        self.channel.setMaximum(16)

        self.control = QSpinBox()
        self.control.setMinimum(0)
        self.control.setMaximum(127)

        self.value = QSpinBox()
        self.value.setMinimum(0)
        self.value.setMaximum(127)

        for name in config["midi"]:
            self.addItem(name)
        
        self.currentTextChanged.connect(self.onTextChange)
        self.setCurrentIndex(0)
    
    def onTextChange(self, device):
        if "defaultChannel" in self.config["midi"][device]:
            self.channel.setValue(self.config["midi"][device]["defaultChannel"])
        
        if self.config["midi"][device]["type"] == "note":
            self.value.setSingleStep(127)
        else:
            self.value.setSingleStep(1)