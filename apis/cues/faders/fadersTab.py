import sys
sys.path.insert(0, '../')

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

TAB_LAYER_NAMES = ["a", "b", "c"]

class FaderTab(QTabWidget):
    def __init__(self, config, widgets, osc):
        super().__init__()
        self.config = config
        self.osc = osc
        self.widgets = widgets

        self.index = 0
        itr = enumerate(self.config["faders"])
        
        for i in range(0, len(TAB_LAYER_NAMES)):
            self.addTab(self.fadersLayer(itr), TAB_LAYER_NAMES[i])
            self.addAction(TabShortcut(self, TAB_LAYER_NAMES[i], i))

    def fadersLayer(self, itr):
        vlayout = QVBoxLayout()

        hlayout = QHBoxLayout()

        for _ in range(0, 4):
            fader = {}
            defaultValue = None
            try:
                _, name = itr.__next__()
                fader["commands"] = self.config["faders"][name]["commands"]
                fader["name"] = QLineEdit(name)
                if ("defaultValue" in self.config["faders"][name]):
                    defaultValue = self.config["faders"][name]["defaultValue"]
            except StopIteration:
                fader["commands"] = []
                fader["name"] = QLineEdit()

            sliderLayout = QVBoxLayout()

            sliderLayout.addWidget(FadersSlider(self.osc, fader, self.index, defaultValue))
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