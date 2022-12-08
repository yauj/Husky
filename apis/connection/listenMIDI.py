from PyQt6.QtWidgets import (
    QMessageBox,
    QPushButton,
)
from util.defaultOSC import MIDIServer

class ListenMidiButton(QPushButton):
    def __init__(self, osc, status, port):
        super().__init__("Connect")
        self.osc = osc
        self.status = status
        self.port = port
        self.osc["serverMidi"] = MIDIServer(self.port)
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
        if (self.osc["serverMidi"].open_input()):
            self.status.setText("Connected!")
            self.status.setStyleSheet("color: green")
            return True
        else:
            self.status.setText("INVALID")
            self.status.setStyleSheet("color: red")

            return False