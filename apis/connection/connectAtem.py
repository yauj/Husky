import traceback
from PyQt6.QtWidgets import (
    QComboBox,
    QMessageBox,
    QPushButton,
)
from pythonosc.udp_client import SimpleUDPClient

class ConnectAtemPort(QComboBox):
    def __init__(self, config, status):
        super().__init__()
        self.status = status

        self.setEditable(True)
        self.setCurrentText(config["atemPort"])
        self.currentTextChanged.connect(self.onChange)

    def onChange(self):
        self.status.setText("Modified")
        self.status.setStyleSheet("color: gray")

class ConnectAtemButton(QPushButton):
    def __init__(self, osc, port, status):
        super().__init__("Set")
        self.osc = osc
        self.port = port
        self.status = status

        try:
            self.init()
        except Exception:
            print(traceback.format_exc())
        self.pressed.connect(self.connect)
        self.setFixedWidth(80)
    
    def connect(self):
        try:
            self.init()
            dlg = QMessageBox(self)
            dlg.setWindowTitle("Atem Connection")
            dlg.setText("Sending Atem OSC commands to local port " + self.port.currentText())
            dlg.exec()
        except Exception as ex:
            print(traceback.format_exc())
            dlg = QMessageBox(self)
            dlg.setWindowTitle("Atem Connection")
            dlg.setText("Error: " + str(ex))
            dlg.exec()

        self.setDown(False)

    def init(self):
        try:
            self.osc["atemClient"] = SimpleUDPClient("0.0.0.0", int(self.port.currentText()))
            self.status.setText("Connected!")
            self.status.setStyleSheet("color: green")
        except Exception as ex:
            self.status.setText("INVALID")
            self.status.setStyleSheet("color: red")
            raise ex