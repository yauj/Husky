import sys
sys.path.insert(0, '../')

from util.defaultOSC import SimpleClient
from PyQt6.QtWidgets import (
    QMessageBox,
    QPushButton,
)

class ConnectOscButton(QPushButton):
    def __init__(self, osc, address, status, mixerName):
        super().__init__("Connect")
        self.osc = osc
        self.address = address
        self.status = status
        self.mixerName = mixerName
        self.init()
        self.pressed.connect(self.connect)
    
    def connect(self):
        if (self.init()):
            dlg = QMessageBox(self)
            dlg.setWindowTitle("X32 Connection")
            dlg.setText("Connected to " + self.mixerName.upper() + " mixer")
            dlg.exec()
        else:
            dlg = QMessageBox(self)
            dlg.setWindowTitle("X32 Connection")
            dlg.setText("Invalid IP Address for " + self.mixerName.upper() + " mixer")
            dlg.exec()
        
        self.setDown(False)

    def init(self):
        self.osc[self.mixerName + "Client"] = SimpleClient(self.mixerName, self.address.currentText())
        if (self.osc[self.mixerName + "Client"].connect()):
            self.status.setText("Connected!")
            self.status.setStyleSheet("color: green")
            return True
        else:
            self.status.setText("INVALID")
            self.status.setStyleSheet("color: red")

            return False