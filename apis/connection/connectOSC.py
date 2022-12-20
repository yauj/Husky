from PyQt6.QtWidgets import (
    QMessageBox,
    QPushButton,
)
from util.defaultOSC import NUM_THREADS, RetryingServer, SimpleClient

class ConnectOscButton(QPushButton):
    def __init__(self, osc, address, status, mixerName, index, widgets, pointIEM):
        super().__init__("Connect")
        self.osc = osc
        self.address = address
        self.status = status
        self.mixerName = mixerName
        self.index = index
        self.widgets = widgets
        self.pointIEM = pointIEM # Whether or not to point IEM client and server to here.

        self.osc[self.mixerName + "Server"] = RetryingServer(10000 + NUM_THREADS + (self.index * 2), mixerName)
        if self.mixerName == "foh" and self.pointIEM:
            self.osc["iemServer"] = self.osc[self.mixerName + "Server"]

        self.init()
        self.pressed.connect(self.connect)
        self.setFixedWidth(80)
    
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
        if self.mixerName == "foh" and self.pointIEM:
            self.osc["iemClient"] = self.osc[self.mixerName + "Client"]

        if (self.osc[self.mixerName + "Client"].connect(self.osc[self.mixerName + "Server"])):
            self.status.setText("Connected!")
            self.status.setStyleSheet("color: green")
            return True
        else:
            self.status.setText("INVALID")
            self.status.setStyleSheet("color: red")
            return False