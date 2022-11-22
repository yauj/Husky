import sys
sys.path.insert(0, '../')

import mido
from util.constants import MIDI_BUS
from PyQt6.QtWidgets import (
    QSlider,
)

class TracksSlider(QSlider):
    def __init__(self, osc, index):
        super().__init__()

        self.midiPort = osc["midi"]
        self.index = index

        self.setRange(0, 127)
        self.setSingleStep(1)
        self.setTickInterval(21)
        self.setTickPosition(QSlider.TickPosition.TicksRight)
        self.valueChanged.connect(self.slider)
        self.setValue(63)
    
    def slider(self):
        self.midiPort.send(mido.Message("control_change", channel = 1, control = self.index, value = self.value()))