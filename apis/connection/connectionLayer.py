from apis.connection.connectAtem import ConnectAtemButton
from apis.connection.connectOSC import ConnectOscButton
from apis.connection.connectMIDI import ConnectMidiButton
from apis.connection.listenMIDI import ListenMidiButton
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

        for idx, mixerName in enumerate(self.config["osc"]):
            hlayout = QHBoxLayout()

            label = QLabel(mixerName.upper() + " Mixer IP Address:" if "iem" in self.config["osc"] else "Mixer IP Address:")
            label.setFixedWidth(150)
            hlayout.addWidget(label)

            address = AddressBox(self.config["osc"][mixerName], validIPs)
            self.widgets["connection"][mixerName + "Client"] = address
            
            hlayout.addWidget(address) 
            hlayout.addWidget(address.status) 
            hlayout.addWidget(ConnectOscButton(self.osc, address, mixerName, idx, self.widgets, "iem" not in self.config["osc"]))

            vlayout.addLayout(hlayout)
        
        hlayout = QHBoxLayout()
        label = QLabel("Atem IP Address:")
        label.setFixedWidth(150)
        hlayout.addWidget(label)

        address = AddressBox(self.config["atemPort"])
        self.widgets["connection"]["atemClient"] = address
        
        hlayout.addWidget(address)  
        hlayout.addWidget(address.status)  
        hlayout.addWidget(ConnectAtemButton(self.osc, address))

        vlayout.addLayout(hlayout)

        hlayout = QHBoxLayout()
        label = QLabel("MIDI Input: ")
        label.setFixedWidth(150)
        hlayout.addWidget(label)

        address = AddressBox(self.config["serverMidi"])
        self.widgets["connection"]["serverMidi"] = address
        
        hlayout.addWidget(address)
        hlayout.addWidget(address.status)
        hlayout.addWidget(ListenMidiButton(self.osc, address))

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
            self.status.setStyleSheet("color: gray")
    
    def addItems(self, texts):
        super().addItems(texts)
        super().setCurrentText(self.currentState["text"])
        self.status.setText(self.currentState["statusText"])
        self.status.setStyleSheet(self.currentState["statusStyle"])