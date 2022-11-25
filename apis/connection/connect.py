import sys
sys.path.insert(0, '../')

from util.defaultOSC import SimpleClient
from PyQt6.QtWidgets import (
    QPushButton,
)

class ConnectButton(QPushButton):
    def __init__(self, osc, address, status, mixerName):
        super().__init__("Connect")
        self.osc = osc
        self.address = address
        self.status = status
        self.mixerName = mixerName
        self.connect()
        self.pressed.connect(self.connect)
    
    def connect(self):
        self.osc[self.mixerName + "Client"] = SimpleClient(self.address.text())
        if (self.osc[self.mixerName + "Client"].connect(self.osc["server"])):
            self.status.setText("Connected!")
            self.status.setStyleSheet("color: green")
        else:
            self.status.setText("INVALID")
            self.status.setStyleSheet("color: red")
        
        self.setDown(False)