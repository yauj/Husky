from PyQt6.QtWidgets import (
    QMessageBox,
    QPushButton,
)
from util.defaultOSC import AtemClient

class ConnectAtemButton(QPushButton):
    def __init__(self, osc, address, status):
        super().__init__("Connect")
        self.osc = osc
        self.address = address
        self.status = status

        self.osc["atemClient"] = AtemClient()

        self.init()
        self.pressed.connect(self.connect)
        self.setFixedWidth(80)
    
    def connect(self):
        if (self.init()):
            dlg = QMessageBox(self)
            dlg.setWindowTitle("Atem Connection")
            dlg.setText("Connected to Atem mixer")
            dlg.exec()
        else:
            dlg = QMessageBox(self)
            dlg.setWindowTitle("Atem Connection")
            dlg.setText("Invalid IP Address for Atem mixer")
            dlg.exec()

        self.setDown(False)

    def init(self):
        if (self.osc["atemClient"].connect(self.address.currentText())):
            self.status.setText("Connected!")
            self.status.setStyleSheet("color: green")
            return True
        else:
            self.status.setText("INVALID")
            self.status.setStyleSheet("color: red")
            return False