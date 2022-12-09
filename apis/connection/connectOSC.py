from apis.misc.miscRouting import syncRouting
from PyQt6.QtWidgets import (
    QMessageBox,
    QPushButton,
)
from util.defaultOSC import SimpleClient

class ConnectOscButton(QPushButton):
    def __init__(self, osc, address, status, mixerName, server, widgets):
        super().__init__("Connect")
        self.osc = osc
        self.address = address
        self.status = status
        self.mixerName = mixerName
        self.server = server
        self.widgets = widgets
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
        
        syncRouting(self.osc, self.mixerName, self.widgets)
        self.setDown(False)

    def init(self):
        self.osc[self.mixerName + "Client"] = SimpleClient(self.mixerName, self.address.currentText())
        if (self.osc[self.mixerName + "Client"].connect(self.server)):
            self.status.setText("Connected!")
            self.status.setStyleSheet("color: green")
            return True
        else:
            self.status.setText("INVALID")
            self.status.setStyleSheet("color: red")

            return False