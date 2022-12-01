import sys
sys.path.insert(0, '../')

from apis.cues.cueFire import CueFireButton, main
import asyncio
from util.constants import KEYS
from PyQt6.QtGui import (
    QAction,
)
from PyQt6.QtWidgets import (
    QComboBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QTabWidget,
    QVBoxLayout,
    QWidget,
)

class CueTab(QTabWidget):
    def __init__(self, osc, widgets):
        super().__init__()
        self.osc = osc
        self.widgets = widgets
        self.cues = []
        
        layers = ["a", "b", "c", "d", "e"]

        for i in range(0, len(layers)):
            self.addTab(self.cuesTriggerLayer(layers[i]), layers[i])
            self.addAction(TabShortcut(self, layers[i], i))

        self.osc["serverMidi"].callback(self.callbackFunction)

    def cuesTriggerLayer(self, page):
        vlayout = QVBoxLayout()

        vlayout.addWidget(QLabel("Fire cues per song"))

        self.widgets["cue"][page] = {}
        for cue in range(0, 10):
            index = str(cue + 1)
            options = {}

            hlayout = QHBoxLayout()
            
            hlayout.addWidget(QLabel(index + ":"))
        
            options["key"] = QComboBox()
            options["key"].setPlaceholderText("Key of Song")
            options["key"].addItem("")
            options["key"].addItems(KEYS)
            hlayout.addWidget(options["key"])

            options["lead"] = QComboBox()
            options["lead"].setPlaceholderText("Vocal Lead")
            options["lead"].addItems(["", "1", "2", "3", "4"])
            hlayout.addWidget(options["lead"])

            snippet = QLineEdit()
            snippet.setPlaceholderText("Snippet Filename")
            snippet.setFixedWidth(150)
            hlayout.addWidget(snippet)
            options["snippet"] = snippet
            self.widgets["cue"][page][index] = snippet

            hlayout.addWidget(CueFireButton(self.widgets, self.osc, index, options))

            vlayout.addLayout(hlayout)
            self.cues.append(options)

        widget = QWidget()
        widget.setLayout(vlayout)
        return widget
    
    def getCues(self):
        return self.cues

    def callbackFunction(self, message):
        if message.channel == 0 and message.control >= 0 and message.control < 10:
            index = (self.currentIndex() * 10) + message.control
            try:
                asyncio.run(main(
                    self.osc,
                    self.cues[index]
                ))
                
                print("Cue " + str(index + 1) + " Fired")
            except Exception as ex:
                print(ex)
        elif message.channel == 0 and message.control == 10:
            self.setCurrentIndex(self.currentIndex() - 1)
        elif message.channel == 0 and message.control == 11:
            self.setCurrentIndex(self.currentIndex() + 1)

class TabShortcut(QAction):
    def __init__(self, cueTab, page, index):
        super().__init__(page, cueTab)
        self.cueTab = cueTab
        self.index = index

        self.triggered.connect(self.tabChange)
        self.setShortcut("ctrl+" + page.lower())

    def tabChange(self):
        self.cueTab.setCurrentIndex(self.index)