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

        self.index = [0]
        itr = enumerate(self.config["cues"]["faders"])
        
        for i in range(0, self.config["cues"]["faderPages"]):
            self.addTab(fadersLayer(config, osc, widgets, self.index, itr), chr(97 + i))
            self.addAction(TabShortcut(self, chr(97 + i), i))

class TabShortcut(QAction):
    def __init__(self, cueTab, page, index):
        super().__init__(page, cueTab)
        self.cueTab = cueTab
        self.index = index

        self.triggered.connect(self.tabChange)
        self.setShortcut("ctrl+" + page.lower())

    def tabChange(self):
        self.cueTab.setCurrentIndex(self.index)

def fadersLayer(config, osc, widgets, index, itr):
    vlayout = QVBoxLayout()

    hlayout = QHBoxLayout()

    for _ in range(0, 4):
        fader = {}
        defaultValue = None
        oscFeedback = None
        try:
            _, name = itr.__next__()
            fader["commands"] = config["cues"]["faders"][name]["commands"]
            fader["name"] = QLineEdit(name)
            if ("defaultValue" in config["cues"]["faders"][name]):
                defaultValue = config["cues"]["faders"][name]["defaultValue"]
            if ("oscFeedback" in config["cues"]["faders"][name]):
                oscFeedback = config["cues"]["faders"][name]["oscFeedback"]
        except StopIteration:
            fader["commands"] = []
            fader["name"] = QLineEdit()

        fader["slider"] = FadersSlider(config, osc, fader, index[0], defaultValue, oscFeedback)

        sliderLayout = QVBoxLayout()
        sliderLayout.addWidget(fader["slider"])
        sliderLayout.addWidget(fader["name"])
        sliderLayout.addWidget(FadersEditButton(config, osc, fader))

        widgets["faders"].append(fader)
        hlayout.addLayout(sliderLayout)

        index[0] = index[0] + 1

    vlayout.addLayout(hlayout)

    widget = QWidget()
    widget.setLayout(vlayout)
    return widget