import traceback
from PyQt6.QtWidgets import (
    QComboBox,
    QMessageBox,
    QPushButton,
)
from pythonosc.udp_client import SimpleUDPClient

class ConnectAtemButton(QPushButton):
    def __init__(self, osc, port):
        super().__init__("Set")
        self.osc = osc
        self.port = port

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
            self.port.connected()
        except Exception as ex:
            self.port.invalid()
            raise ex