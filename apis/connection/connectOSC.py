from PyQt6.QtWidgets import (
    QComboBox,
    QHBoxLayout,
    QLabel,
    QMessageBox,
    QPushButton,
)
from util.constants import START_PORT, VALID_MIXER_TYPES
from util.defaultOSC import NUM_THREADS, RetryingServer, SimpleClient

class OscHLayout(QHBoxLayout):
    def __init__(self, config, osc, widgets, mixerName, index, options, pointIEM):
        super().__init__()
        self.config = config
        self.osc = osc
        self.widgets = widgets
        self.mixerName = mixerName
        self.index = index
        self.options = options
        self.pointIEM = pointIEM

        self.osc[self.mixerName + "Server"] = RetryingServer(START_PORT + 1 + NUM_THREADS + (self.index * 2), self.mixerName)
        if self.mixerName == "foh" and self.pointIEM:
            self.osc["iemServer"] = self.osc[self.mixerName + "Server"]

        label = QLabel(mixerName.upper() + " Mixer IP Address:")
        label.setFixedWidth(150)
        self.addWidget(label)

        self.currentState = {
            "type": config["osc"][mixerName]["type"],
            "ip": config["osc"][mixerName]["ip"],
            "statusText": "",
            "statusStyle": ""
        }

        self.status = QLabel()
        self.status.setFixedWidth(80)

        self.address = QComboBox()
        self.address.setEditable(True)
        self.address.setCurrentText(config["osc"][mixerName]["ip"])
        self.address.currentTextChanged.connect(self.onAddressChange)

        self.mixerType = QComboBox()
        self.mixerType.addItems(VALID_MIXER_TYPES)
        self.mixerType.setCurrentText(config["osc"][mixerName]["type"])
        self.mixerType.currentTextChanged.connect(self.onMixerChange)
        self.mixerType.setFixedWidth(80)
        self.reinitOptions()

        self.connectButton = QPushButton("Connect")
        self.init()
        self.connectButton.pressed.connect(self.connect)
        self.connectButton.setFixedWidth(80)

        self.addWidget(self.mixerType)
        self.addWidget(self.address)
        self.addWidget(self.status)
        self.addWidget(self.connectButton)

    def onMixerChange(self, text):
        if text == self.currentState["type"]:
            self.status.setText(self.currentState["statusText"])
            self.status.setStyleSheet(self.currentState["statusStyle"])
        else:
            self.status.setText("Modified")
            self.status.setStyleSheet("color: gray")
        
        self.reinitOptions()

    def onAddressChange(self, text):
        if text == self.currentState["ip"]:
            self.status.setText(self.currentState["statusText"])
            self.status.setStyleSheet(self.currentState["statusStyle"])
        else:
            self.status.setText("Modified")
            self.status.setStyleSheet("color: gray")
    
    def reinitOptions(self):
        while self.address.itemText(0) != "":
            self.address.removeItem(0)
        if self.mixerType.currentText() in ["X32"]:
            self.address.addItems(self.options["X32"])
        elif self.mixerType.currentText() in ["XR18", "XR16", "XR12"]:
            self.address.addItems(self.options["X-Air"])
        self.address.setCurrentText(self.currentState["ip"])
    
    def connect(self):
        if (self.init()):
            dlg = QMessageBox()
            dlg.setWindowTitle("Connection")
            dlg.setText("Connected to " + self.mixerName.upper() + " mixer")
            dlg.exec()
        else:
            dlg = QMessageBox()
            dlg.setWindowTitle("Connection")
            dlg.setText("Invalid IP Address for " + self.mixerName.upper() + " mixer")
            dlg.exec()

        self.connectButton.setDown(False)

    def init(self):
        self.currentState["type"] = self.mixerType.currentText()
        self.currentState["ip"] = self.address.currentText()

        self.osc[self.mixerName + "Client"] = SimpleClient(self.mixerName, self.address.currentText(), self.mixerType.currentText())
        if self.mixerName == "foh" and self.pointIEM:
            self.osc["iemClient"] = self.osc[self.mixerName + "Client"]

        if (self.osc[self.mixerName + "Client"].connect(self.osc[self.mixerName + "Server"])):
            self.currentState["statusText"] = "Connected!"
            self.currentState["statusStyle"] = "color: green"
            self.status.setText(self.currentState["statusText"])
            self.status.setStyleSheet(self.currentState["statusStyle"])
            return True
        else:
            self.currentState["statusText"] = "INVALID"
            self.currentState["statusStyle"] = "color: red"
            self.status.setText(self.currentState["statusText"])
            self.status.setStyleSheet(self.currentState["statusStyle"])
            return False