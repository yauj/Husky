from PyQt6.QtWidgets import (
    QMessageBox,
    QPushButton,
)
from util.defaultOSC import MIDIClient

class ConnectMidiButton(QPushButton):
    def __init__(self, osc, name, port):
        super().__init__("Connect")
        self.osc = osc
        self.name = name
        self.port = port
        self.init(True)
        self.pressed.connect(self.connect)
        self.setFixedWidth(80)
    
    def connect(self):
        if (self.init()):
            dlg = QMessageBox(self)
            dlg.setWindowTitle("MIDI Connection")
            dlg.setText("Connected to " + self.port.currentText() + " port")
            dlg.exec()
        else:
            dlg = QMessageBox(self)
            dlg.setWindowTitle("MIDI Connection")
            dlg.setText("Unable to connect to " + self.port.currentText() + " port")
            dlg.exec()
        
        self.setDown(False)

    def init(self, init = False):
        self.osc[self.name + "Midi"] = MIDIClient(self.port.currentText())

        if init:
            currentText = self.port.currentText()
            self.port.addItems(self.osc[self.name + "Midi"].get_output_names())
            self.port.setCurrentText(currentText)

        if (self.osc[self.name + "Midi"].open_output()):
            self.port.connected()
            return True
        else:
            self.port.invalid()
            return False