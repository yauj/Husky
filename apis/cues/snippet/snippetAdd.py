import sys
import traceback
sys.path.insert(0, '../')

from apis.snippets.saveSingle import appendSettingsToTextbox
from PyQt6.QtWidgets import (
    QCheckBox,
    QComboBox,
    QDialog,
    QHBoxLayout,
    QLabel,
    QMessageBox,
    QPushButton,
    QSpinBox,
    QTabWidget,
    QVBoxLayout,
    QWidget,
)
from util.constants import ALL_BUSES, ALL_CHANNELS, AUX_CHANNELS, ODD_BUSES, SETTINGS

class SnippetAddButton(QPushButton):
    def __init__(self, osc, textbox):
        super().__init__("Add Commands")
        self.osc = osc
        self.textbox = textbox
        self.pressed.connect(self.clicked)
    
    def clicked(self):
        SnippetAddDialog(self.osc, self.textbox).exec()
        self.setDown(False)

class SnippetAddDialog(QDialog):
    def __init__(self, osc, textbox):
        super().__init__()
        self.osc = osc
        self.textbox = textbox

        layout = QVBoxLayout()
        tabs = QTabWidget()
        tabs.addTab(self.fohLayer(), "FOH Mixer")
        tabs.addTab(self.iemLayer(), "IEM Mixer")
        tabs.addTab(self.audioLayer(), "Audio MIDI")
        tabs.addTab(self.lightLayer(), "Light MIDI")
        layout.addWidget(tabs)

        self.setLayout(layout)

    def fohLayer(self):
        vlayout = QVBoxLayout()

        hlayout = QHBoxLayout()
        hlayout.addWidget(QLabel("Channel: "))
        self.channel = QComboBox()
        self.channel.addItems(ALL_CHANNELS)
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

        vlayout.addWidget(AddFOHButton(self.osc, self.textbox, self.channel, self.settings, fader))

        widget = QWidget()
        widget.setLayout(vlayout)
        return widget

    def iemLayer(self):
        vlayout = QVBoxLayout()

        hlayout = QHBoxLayout()
        hlayout.addWidget(QLabel("Bus: "))
        bus = QComboBox()
        bus.addItems(ALL_BUSES)
        hlayout.addWidget(bus)
        vlayout.addLayout(hlayout)

        vlayout.addWidget(AddIEMButton(self.osc, self.textbox, bus))

        widget = QWidget()
        widget.setLayout(vlayout)
        return widget

    def audioLayer(self):
        vlayout = QVBoxLayout()

        hlayout = QHBoxLayout()
        hlayout.addWidget(QLabel("Channel: "))
        channel = QSpinBox()
        channel.setMinimum(1)
        channel.setMaximum(16)
        channel.setValue(2)
        hlayout.addWidget(channel)
        vlayout.addLayout(hlayout)

        hlayout = QHBoxLayout()
        hlayout.addWidget(QLabel("Control: "))
        control = QSpinBox()
        control.setMinimum(0)
        control.setMaximum(127)
        hlayout.addWidget(control)
        vlayout.addLayout(hlayout)

        hlayout = QHBoxLayout()
        hlayout.addWidget(QLabel("Value: "))
        value = QSpinBox()
        value.setMinimum(0)
        value.setMaximum(127)
        hlayout.addWidget(value)
        vlayout.addLayout(hlayout)

        vlayout.addWidget(AddMIDIButton(self.textbox, "audio", channel, control, value))

        widget = QWidget()
        widget.setLayout(vlayout)
        return widget

    def lightLayer(self):
        vlayout = QVBoxLayout()

        hlayout = QHBoxLayout()
        hlayout.addWidget(QLabel("Channel: "))
        channel = QSpinBox()
        channel.setMinimum(1)
        channel.setMaximum(16)
        channel.setValue(15)
        hlayout.addWidget(channel)
        vlayout.addLayout(hlayout)

        hlayout = QHBoxLayout()
        hlayout.addWidget(QLabel("Control: "))
        control = QSpinBox()
        control.setMinimum(0)
        control.setMaximum(127)
        hlayout.addWidget(control)
        vlayout.addLayout(hlayout)

        hlayout = QHBoxLayout()
        hlayout.addWidget(QLabel("Value: "))
        value = QSpinBox()
        value.setMinimum(0)
        value.setMaximum(127)
        value.setSingleStep(127)
        hlayout.addWidget(value)
        vlayout.addLayout(hlayout)

        vlayout.addWidget(AddMIDIButton(self.textbox, "light", channel, control, value))

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
        else:
            self.settings["HPF"].setEnabled(True)
            self.settings["HPF"].setChecked(self.settings["EQ"].isChecked())
            self.settings["Dynamics"].setEnabled(True)

class AddFOHButton(QPushButton):
    def __init__(self, osc, textbox, channel, settings, fader):
        super().__init__("Add")
        self.osc = osc
        self.textbox = textbox
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
            print(traceback.format_exc())
            dlg = QMessageBox(self)
            dlg.setWindowTitle("Add")
            dlg.setText("Error: " + str(ex))
            dlg.exec()

        self.setDown(False)

    def main(self):
        settings = {}
        for category in self.settings:
            if self.settings[category].isChecked():
                for param in SETTINGS[category]:
                    settings[self.channel.currentText() + param] = None

        if self.fader.isChecked():
            settings[self.channel.currentText() + "/mix/fader"] = None

        if len(settings) > 0:
            appendSettingsToTextbox(self.osc, self.textbox, "foh", settings)

class AddIEMButton(QPushButton):
    def __init__(self, osc, textbox, bus):
        super().__init__("Add")
        self.osc = osc
        self.textbox = textbox
        self.bus = bus
        self.pressed.connect(self.clicked)
    
    def clicked(self):
        try:
            self.main()
            
            dlg = QMessageBox(self)
            dlg.setWindowTitle("Add")
            dlg.setText("Settings Added")
            dlg.exec()
        except Exception as ex:
            print(traceback.format_exc())
            dlg = QMessageBox(self)
            dlg.setWindowTitle("Add")
            dlg.setText("Error: " + str(ex))
            dlg.exec()

        self.setDown(False)

    def main(self):
        settings = {}
        for channel in ALL_CHANNELS:
            prefix = channel + "/mix/" + self.bus.currentText()

            settings[prefix + "/on"] = None
            settings[prefix + "/level"] = None

            if self.bus.currentText() in ODD_BUSES:
                settings[prefix + "/pan"] = None
        
        appendSettingsToTextbox(self.osc, self.textbox, "iem", settings)

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
            self.textbox.append("midi " + self.type + " " + str(self.channel.value()) + " " + str(self.control.value()) + " " + str(self.value.value()))
            
            dlg = QMessageBox(self)
            dlg.setWindowTitle("Add")
            dlg.setText("Settings Added")
            dlg.exec()
        except Exception as ex:
            print(traceback.format_exc())
            dlg = QMessageBox(self)
            dlg.setWindowTitle("Add")
            dlg.setText("Error: " + str(ex))
            dlg.exec()

        self.setDown(False)