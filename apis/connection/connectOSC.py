from PyQt6.QtWidgets import (
    QComboBox,
    QHBoxLayout,
    QLabel,
    QMessageBox,
    QPushButton,
)
from util.constants import START_PORT, VALID_IEM_MIXER_TYPES, VALID_MIXER_TYPES
from util.defaultOSC import NUM_THREADS, RetryingServer, SimpleClient

class OscHLayout(QHBoxLayout):
    def __init__(self, config, osc, widgets, mixerName, index, options, otherLayouts = None):
        super().__init__()
        self.config = config
        self.osc = osc
        self.widgets = widgets
        self.mixerName = mixerName
        self.index = index
        self.options = options
        self.otherLayouts = otherLayouts

        self.osc[self.mixerName + "Server"] = RetryingServer(START_PORT + 1 + NUM_THREADS + (self.index * 2), self.mixerName)
        if self.mixerName == "foh" and "iem" not in self.config["osc"]:
            self.osc["iemServer"] = self.osc["fohServer"]

        self.label = QLabel(mixerName.upper() + " Mixer IP Address:")
        self.label.setFixedWidth(150)
        self.addWidget(self.label)

        self.currentState = {
            "type": "",
            "ip": "",
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
        if self.mixerName == "iem":
            self.mixerType.addItems(VALID_IEM_MIXER_TYPES)
        else:
            self.mixerType.addItems(VALID_MIXER_TYPES)
        self.mixerType.setCurrentText(config["osc"][mixerName]["type"])
        self.mixerType.currentTextChanged.connect(self.onMixerChange)
        self.mixerType.setFixedWidth(80)

        self.connectButton = QPushButton("Connect")
        self.init()
        self.connectButton.pressed.connect(self.connect)
        self.connectButton.setFixedWidth(80)

        self.reinitOptions()

        self.addWidget(self.mixerType)
        self.addWidget(self.address)
        self.addWidget(self.status)
        self.addWidget(self.connectButton)

    def onMixerChange(self, text):
        self.reinitOptions()

        if text == self.currentState["type"]:
            self.status.setText(self.currentState["statusText"])
            self.status.setStyleSheet(self.currentState["statusStyle"])
        else:
            self.status.setText("Modified")
            self.status.setStyleSheet("color: yellow")

    def onAddressChange(self, text):
        if text == self.currentState["ip"]:
            self.status.setText(self.currentState["statusText"])
            self.status.setStyleSheet(self.currentState["statusStyle"])
        else:
            self.status.setText("Modified")
            self.status.setStyleSheet("color: yellow")
    
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
        self.osc[self.mixerName + "Client"] = SimpleClient(self.mixerName, self.address.currentText(), self.mixerType.currentText())
        if self.mixerName == "foh" and "iem" not in self.config["osc"]:
            self.osc["iemClient"] = self.osc["fohClient"]
        
        if self.otherLayouts is not None:
            for layout in self.otherLayouts:
                layout.iemSetEnabled(self.mixerType.currentText(), self.address.currentText())

            if self.mixerType.currentText() in VALID_IEM_MIXER_TYPES:
                self.widgets["misc"]["routing"].setEnabled(True)
                if "iem" in self.config["osc"]:
                    self.widgets["misc"]["transfer"].setEnabled(True)
                self.widgets["misc"]["talkback"].setEnabled(True)
            else:
                self.widgets["misc"]["routing"].setEnabled(False)
                if "iem" in self.config["osc"]:
                    self.widgets["misc"]["transfer"].setEnabled(False)
                self.widgets["misc"]["talkback"].setEnabled(False)

        self.currentState["type"] = self.mixerType.currentText()
        self.currentState["ip"] = self.address.currentText()

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
    
    def iemSetEnabled(self, type, ip):
        if type in VALID_IEM_MIXER_TYPES:
            if self.mixerType.currentIndex() == -1:
                self.mixerType.setEnabled(True)
                self.address.setEnabled(True)
                self.connectButton.setEnabled(True)

                self.label.setStyleSheet("")
                self.mixerType.setCurrentText(type)
                self.address.setCurrentText(ip)
                self.init()
        else:
            self.mixerType.setEnabled(False)
            self.address.setEnabled(False)
            self.connectButton.setEnabled(False)

            self.label.setStyleSheet("color: gray")
            self.mixerType.setCurrentIndex(-1)
            self.address.setCurrentIndex(-1)
            self.status.setText("disabled")
            self.status.setStyleSheet("color: gray")

            self.osc["iemClient"] = self.osc["fohClient"]