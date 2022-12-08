import sys
import traceback
sys.path.insert(0, '../')

from apis.cues.cueFire import CueFireButton, main
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

TAB_LAYER_NAMES = ["a", "b", "c", "d", "e"]

class CueTab(QTabWidget):
    def __init__(self, osc, widgets):
        super().__init__()
        self.osc = osc
        self.widgets = widgets
        self.prevIndex = [None]
        
        for i in range(0, len(TAB_LAYER_NAMES)):
            self.addTab(self.cuesTriggerLayer(TAB_LAYER_NAMES[i], i), TAB_LAYER_NAMES[i])
            self.addAction(TabShortcut(self, TAB_LAYER_NAMES[i], i))

        self.osc["serverMidi"].callback(self.callbackFunction)

    def cuesTriggerLayer(self, pageName, pageIndex):
        vlayout = QVBoxLayout()

        self.widgets["cueSnippet"][pageName] = {}
        for cue in range(0, 10):
            index = (pageIndex * 10) + cue
            printIndex = str(cue + 1)
            options = {}

            hlayout = QHBoxLayout()

            options["label"] = QLabel(printIndex + ":")
            hlayout.addWidget(options["label"])
        
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
            self.widgets["cueSnippet"][pageName][printIndex] = snippet

            hlayout.addWidget(CueFireButton(self.osc, self.prevIndex, index, printIndex, self.widgets["cues"]))

            vlayout.addLayout(hlayout)
            self.widgets["cues"].append(options)

        widget = QWidget()
        widget.setLayout(vlayout)
        return widget

    def callbackFunction(self, message):
        if message.channel == 4 and message.value > 0:
            if message.control >= 0 and message.control < 10:
                index = (self.currentIndex() * 10) + message.control
                try:
                    main(
                        self.osc,
                        self.prevIndex,
                        index,
                        self.widgets["cues"]
                    )
                    
                    print("Cue " + TAB_LAYER_NAMES[self.currentIndex()] + str(message.control + 1) + " Fired")
                except Exception:
                    print(traceback.format_exc())
            elif message.control == 10:
                self.setCurrentIndex(self.currentIndex() - 1)
            elif message.control == 11:
                self.setCurrentIndex(self.currentIndex() + 1)
            elif message.control == 12 and message.value <= len(TAB_LAYER_NAMES):
                self.setCurrentIndex(message.value - 1)

class TabShortcut(QAction):
    def __init__(self, cueTab, page, index):
        super().__init__(page, cueTab)
        self.cueTab = cueTab
        self.index = index

        self.triggered.connect(self.tabChange)
        self.setShortcut("ctrl+" + page.lower())

    def tabChange(self):
        self.cueTab.setCurrentIndex(self.index)