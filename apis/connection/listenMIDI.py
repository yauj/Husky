import sys
sys.path.insert(0, '../')

from util.defaultOSC import MIDIServer
from PyQt6.QtWidgets import (
    QMessageBox,
    QPushButton,
)

class ListenMidiButton(QPushButton):
    def __init__(self, osc, status, port):
        super().__init__("Connect")
        self.osc = osc
        self.status = status
        self.port = port
        self.init()
        self.pressed.connect(self.connect)
    
    def connect(self):
        if (self.init()):
            dlg = QMessageBox(self)
            dlg.setWindowTitle("MIDI Connection")
            dlg.setText("Listening to " + self.port.currentText() + " port")
            dlg.exec()
        else:
            dlg = QMessageBox(self)
            dlg.setWindowTitle("MIDI Connection")
            dlg.setText("Unable to listen to " + self.port.currentText() + " port")
            dlg.exec()
        
        self.setDown(False)

    def init(self):
        if ("serverMidi" in self.osc):
            self.osc["serverMidi"].close()

        self.osc["serverMidi"] = MIDIServer(self.port.currentText())
        if (self.osc["serverMidi"].open_input()):
            self.status.setText("Connected!")
            self.status.setStyleSheet("color: green")
            return True
        else:
            self.status.setText("INVALID")
            self.status.setStyleSheet("color: red")
            self.osc["serverMidi"] = None

            return False