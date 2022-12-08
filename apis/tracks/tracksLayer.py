import sys
sys.path.insert(0, '../')

from apis.tracks.tracksSlider import TracksSlider
from PyQt6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QVBoxLayout,
    QWidget,
)

class TracksLayer(QWidget):
    def __init__(self, osc):
        super().__init__()
        self.osc = osc

        vlayout = QVBoxLayout()

        vlayout.addWidget(QLabel("Volume Sliders for tracks"))

        hlayout = QHBoxLayout()

        sliders = ["BGVS", "Choir", "Keys", "EG", "Bass", "Drums"]

        for i in range (0, len(sliders)):
            sliderLayout = QVBoxLayout()

            sliderLayout.addWidget(TracksSlider(self.osc, i + 50))
            sliderLayout.addWidget(QLabel(sliders[i]))

            hlayout.addLayout(sliderLayout)

        vlayout.addLayout(hlayout)

        self.setLayout(vlayout)