from apis.connection.connectAtem import ConnectAtemButton
from apis.connection.connectOSC import OscHLayout
from apis.connection.connectMIDI import ConnectMidiButton
from apis.connection.listenMIDI import MidiInputsButton
from PyQt6.QtWidgets import (
    QComboBox,
    QHBoxLayout,
    QLabel,
    QVBoxLayout,
    QWidget,
)
from util.defaultOSC import AvailableIPs

class ConnectionLayer(QWidget):
    def __init__(self, config, widgets, osc):
        super().__init__()
        self.config = config
        self.widgets = widgets
        self.osc = osc

        vlayout = QVBoxLayout()

        validIPs = AvailableIPs().get()
        self.otherLines = []

        fohLine = OscHLayout(self.config, self.osc, self.widgets, "foh", 0, validIPs, self.otherLines)
        vlayout.addLayout(fohLine)

        idx = 1
        for mixerName in self.config["osc"]:
            if mixerName != "foh":
                layout = OscHLayout(self.config, self.osc, self.widgets, mixerName, idx, validIPs)
                self.otherLines.append(layout)
                vlayout.addLayout(layout)
                idx = idx + 1

        hlayout = QHBoxLayout()
        label = QLabel("AtemOSC Port:")
        label.setFixedWidth(150)
        hlayout.addWidget(label)

        address = AddressBox(self.config["atemPort"])
        self.widgets["connection"]["atemClient"] = address
        
        hlayout.addWidget(address)  
        hlayout.addWidget(address.status)  
        hlayout.addWidget(ConnectAtemButton(self.osc, address))

        vlayout.addLayout(hlayout)

        for name in self.config["midi"]:
            hlayout = QHBoxLayout()
            label = QLabel(name.capitalize() + " MIDI: ")
            label.setFixedWidth(150)
            hlayout.addWidget(label)

            address = AddressBox(self.config["midi"][name]["default"])
            self.widgets["connection"][name + "Midi"] = address
            
            hlayout.addWidget(address)
            hlayout.addWidget(address.status)
            hlayout.addWidget(ConnectMidiButton(self.osc, name, address))

            vlayout.addLayout(hlayout)

        vlayout.addWidget(MidiInputsButton(self.osc, self.widgets))

        self.setLayout(vlayout)

class AddressBox(QComboBox):
    def __init__(self, initVal, options = None):
        super().__init__()
        self.status = QLabel()
        self.status.setFixedWidth(80)

        self.currentState = {
            "text": initVal,
            "statusText": "",
            "statusStyle": ""
        }

        self.setEditable(True)
        if options is not None:
            self.addItems(options)
        self.setCurrentText(initVal)
        self.currentTextChanged.connect(self.onChange)
    
    def connected(self):
        self.currentState["statusText"] = "Connected!"
        self.currentState["statusStyle"] = "color: green"
        self.status.setText(self.currentState["statusText"])
        self.status.setStyleSheet(self.currentState["statusStyle"])

    def invalid(self):
        self.currentState["statusText"] = "INVALID"
        self.currentState["statusStyle"] = "color: red"
        self.status.setText(self.currentState["statusText"])
        self.status.setStyleSheet(self.currentState["statusStyle"])

    def onChange(self, text):
        if text == self.currentState["text"]:
            self.status.setText(self.currentState["statusText"])
            self.status.setStyleSheet(self.currentState["statusStyle"])
        else:
            self.status.setText("Modified")
            self.status.setStyleSheet("color: yellow")
    
    def addItems(self, texts):
        super().addItems(texts)
        super().setCurrentText(self.currentState["text"])
        self.status.setText(self.currentState["statusText"])
        self.status.setStyleSheet(self.currentState["statusStyle"])