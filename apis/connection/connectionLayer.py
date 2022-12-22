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
from util.defaultOSC import AvailableAtemIPs, AvailableIPs

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

            address = QComboBox()
            address.setEditable(True)
            address.addItems(validIPs)
            address.setCurrentText(self.config["osc"][mixerName])
            self.widgets["connection"][mixerName + "Client"] = address
            hlayout.addWidget(address)

            status = QLabel()
            status.setFixedWidth(80)
            hlayout.addWidget(status)
            
            hlayout.addWidget(ConnectOscButton(self.osc, address, status, mixerName, idx, self.widgets, "iem" not in self.config["osc"]))

            vlayout.addLayout(hlayout)
        
        hlayout = QHBoxLayout()
        label = QLabel("Atem IP Address:")
        label.setFixedWidth(150)
        hlayout.addWidget(label)

        address = QComboBox()
        address.setEditable(True)
        address.addItems(AvailableAtemIPs().get())
        address.setCurrentText(self.config["atem"])
        self.widgets["connection"]["atemClient"] = address
        hlayout.addWidget(address)

        status = QLabel()
        status.setFixedWidth(80)
        hlayout.addWidget(status)
        
        hlayout.addWidget(ConnectAtemButton(self.osc, address, status))

        vlayout.addLayout(hlayout)

        hlayout = QHBoxLayout()
        label = QLabel("MIDI Input: ")
        label.setFixedWidth(150)
        hlayout.addWidget(label)

        port = QComboBox()
        port.setEditable(True)
        port.setCurrentText(self.config["serverMidi"])
        self.widgets["connection"]["serverMidi"] = port
        hlayout.addWidget(port)

        status = QLabel()
        status.setFixedWidth(80)
        hlayout.addWidget(status)

        hlayout.addWidget(ListenMidiButton(self.osc, status, port))

        port.addItems(self.osc["serverMidi"].get_input_names())
        port.setCurrentText(self.config["serverMidi"])

        vlayout.addLayout(hlayout)
        
        for name in self.config["midi"]:
            hlayout = QHBoxLayout()
            label = QLabel(name.capitalize() + " MIDI: ")
            label.setFixedWidth(150)
            hlayout.addWidget(label)

            port = QComboBox()
            port.setEditable(True)
            port.setCurrentText(self.config["midi"][name]["default"])
            self.widgets["connection"][name + "Midi"] = port
            hlayout.addWidget(port)

            status = QLabel()
            status.setFixedWidth(80)
            hlayout.addWidget(status)

            hlayout.addWidget(ConnectMidiButton(self.osc, name, status, port))

            port.addItems(self.osc[name + "Midi"].get_output_names())
            port.setCurrentText(self.config["midi"][name]["default"])

            vlayout.addLayout(hlayout)

        self.setLayout(vlayout)