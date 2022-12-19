from apis.cues.faders.fadersEdit import FadersEditButton
from apis.cues.faders.fadersSlider import FadersSlider
from PyQt6.QtGui import (
    QAction,
)
from PyQt6.QtWidgets import (
    QHBoxLayout,
    QLineEdit,
    QTabWidget,
    QVBoxLayout,
    QWidget,
)

class FaderTab(QTabWidget):
    def __init__(self, config, widgets, osc):
        super().__init__()
        self.config = config
        self.osc = osc
        self.widgets = widgets

        self.index = 0
        itr = enumerate(self.config["cues"]["faders"])
        
        for i in range(0, self.config["cues"]["faderPages"]):
            self.addTab(self.fadersLayer(itr), chr(97 + i))
            self.addAction(TabShortcut(self, chr(97 + i), i))

    def fadersLayer(self, itr):
        vlayout = QVBoxLayout()

        hlayout = QHBoxLayout()

        for _ in range(0, 4):
            fader = {}
            defaultValue = None
            oscFeedback = None
            try:
                _, name = itr.__next__()
                fader["commands"] = self.config["cues"]["faders"][name]["commands"]
                fader["name"] = QLineEdit(name)
                if ("defaultValue" in self.config["cues"]["faders"][name]):
                    defaultValue = self.config["cues"]["faders"][name]["defaultValue"]
                if ("oscFeedback" in self.config["cues"]["faders"][name]):
                    oscFeedback = self.config["cues"]["faders"][name]["oscFeedback"]
            except StopIteration:
                fader["commands"] = []
                fader["name"] = QLineEdit()

            fader["slider"] = FadersSlider(self.config, self.osc, fader, self.index, defaultValue, oscFeedback)

            sliderLayout = QVBoxLayout()
            sliderLayout.addWidget(fader["slider"])
            sliderLayout.addWidget(fader["name"])
            sliderLayout.addWidget(FadersEditButton(self.osc, fader))

            self.widgets["faders"].append(fader)
            hlayout.addLayout(sliderLayout)

            self.index = self.index + 1

        vlayout.addLayout(hlayout)

        widget = QWidget()
        widget.setLayout(vlayout)
        return widget

class TabShortcut(QAction):
    def __init__(self, cueTab, page, index):
        super().__init__(page, cueTab)
        self.cueTab = cueTab
        self.index = index

        self.triggered.connect(self.tabChange)
        self.setShortcut("ctrl+" + page.lower())

    def tabChange(self):
        self.cueTab.setCurrentIndex(self.index)