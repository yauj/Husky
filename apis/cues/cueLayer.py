from apis.cues.cueClear import CueClearButton
from apis.cues.cueLoad import CueLoadButton
from apis.cues.cueSave import CueSaveButton
from apis.cues.cueTabs import CueTab, cuesTriggerLayer
from apis.cues.faders.fadersReset import FadersResetButton
from apis.cues.faders.fadersTab import FaderTab, fadersLayer
from PyQt6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QTabWidget,
    QVBoxLayout,
    QWidget,
)

class CueLayer(QTabWidget):
    def __init__(self, config, widgets, osc):
        super().__init__()
        self.config = config
        self.widgets = widgets
        self.osc = osc

        vlayout = QVBoxLayout()

        tabs = self.cueTab()
        faders = self.faderTab()

        hlayout = QHBoxLayout()
        hlayout.addWidget(CueLoadButton(self.widgets))
        hlayout.addWidget(CueSaveButton(self.config, self.widgets))
        vlayout.addLayout(hlayout)

        subLayer = QTabWidget()
        subLayer.addTab(tabs, "Cues")
        subLayer.addTab(faders, "Faders")

        vlayout.addWidget(subLayer)

        self.setLayout(vlayout)

    def cueTab(self):
        vlayout = QVBoxLayout()

        hlayout = QHBoxLayout()
        hlayout.addWidget(QLabel("Fire Cues. Green indicates last cue fired was successful. Red indicates failure."))
        hlayout.addWidget(CueClearButton(self.widgets))
        vlayout.addLayout(hlayout)

        if "cuePages" not in self.config["cues"] or self.config["cues"]["cuePages"] < 2:
            self.prevIndex = [None]
            vlayout.addWidget(cuesTriggerLayer(self.config, self.osc, self.widgets, self.prevIndex, 0))
        else:
            vlayout.addWidget(CueTab(self.config, self.osc, self.widgets))

        widget = QWidget()
        widget.setLayout(vlayout)
        return widget
    
    def faderTab(self):
        vlayout = QVBoxLayout()

        hlayout = QHBoxLayout()
        hlayout.addWidget(QLabel("Configurable OSC and MIDI Faders"))
        hlayout.addWidget(FadersResetButton(self.config, self.widgets))
        vlayout.addLayout(hlayout)

        if "faderPages" not in self.config["cues"] or self.config["cues"]["faderPages"] < 2:
            vlayout.addWidget(fadersLayer(self.config, self.osc, self.widgets, [0], enumerate(self.config["cues"]["faders"])))
        else:
            vlayout.addWidget(FaderTab(self.config, self.widgets, self.osc))

        widget = QWidget()
        widget.setLayout(vlayout)
        return widget