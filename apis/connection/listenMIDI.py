from PyQt6.QtWidgets import (
    QMessageBox,
    QPushButton,
)
from util.defaultOSC import MIDIServer

class ListenMidiButton(QPushButton):
    def __init__(self, osc, port):
        super().__init__("Connect")
        self.osc = osc
        self.port = port
        self.osc["serverMidi"] = MIDIServer(self.port)
        self.init(True)
        self.pressed.connect(self.connect)
        self.setFixedWidth(80)
    
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

    def init(self, init = False):
        if init:
            currentText = self.port.currentText()
            self.port.addItems(self.osc["serverMidi"].get_input_names())
            self.port.setCurrentText(currentText)

        if (self.osc["serverMidi"].open_input()):
            self.port.connected()
            return True
        else:
            self.port.invalid()
            return False