import sys
sys.path.insert(0, '../')

import mido
from util.constants import MIDI_BUS
from PyQt6.QtWidgets import (
    QSlider,
)

class TracksSlider(QSlider):
    def __init__(self, index):
        super().__init__()

        self.index = index

        self.midiPort = mido.Backend("mido.backends.rtmidi").open_output(MIDI_BUS)

        self.setRange(0, 127)
        self.setSingleStep(1)
        self.valueChanged.connect(self.slider)
    
    def slider(self):
        self.midiPort.send(mido.Message("control_change", channel = 1, control = self.index, value = self.value()))