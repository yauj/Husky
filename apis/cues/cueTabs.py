from apis.cues.cueFire import CueFireButton, main
from apis.cues.cueSnippet import CueSnippetButton
from PyQt6.QtGui import (
    QAction,
)
from PyQt6.QtWidgets import (
    QComboBox,
    QHBoxLayout,
    QLabel,
    QScrollArea,
    QTabWidget,
    QVBoxLayout,
    QWidget,
)
import traceback
from util.constants import KEYS

class CueTab(QTabWidget):
    def __init__(self, config, osc, widgets):
        super().__init__()
        self.config = config
        self.osc = osc
        self.widgets = widgets
        self.prevIndex = [None]
        
        for i in range(0, self.config["cues"]["cuePages"]):
            self.addTab(cuesTriggerLayer(config, osc, widgets, self.prevIndex, i), chr(97 + i))
            self.addAction(TabShortcut(self, chr(97 + i), i))

        self.osc["serverMidi"].callback(self.callbackFunction)

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
                    
                    print("Cue " + chr(97 + self.currentIndex()) + str(message.control + 1) + " Fired")
                except Exception:
                    print(traceback.format_exc())
            elif message.control == 10:
                self.setCurrentIndex(self.currentIndex() - 1)
            elif message.control == 11:
                self.setCurrentIndex(self.currentIndex() + 1)
            elif message.control == 12 and message.value <= self.config["cues"]["cuePages"]:
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

def cuesTriggerLayer(config, osc, widgets, prevIndex, pageIndex):
    vlayout = QVBoxLayout()

    for cue in range(0, 10):
        index = (pageIndex * 10) + cue
        printIndex = str(cue + 1)
        options = {}

        hlayout = QHBoxLayout()

        options["label"] = QLabel(printIndex + ":")
        options["label"].setFixedWidth(20)
        hlayout.addWidget(options["label"])
    
        options["key"] = QComboBox()
        options["key"].setFixedWidth(120)
        options["key"].setPlaceholderText("Key of Song")
        options["key"].addItem("")
        options["key"].addItems(KEYS)
        hlayout.addWidget(options["key"])

        options["lead"] = QComboBox()
        options["lead"].setFixedWidth(120)
        options["lead"].setPlaceholderText("Vocal Lead")
        options["lead"].addItems(["", "1", "2", "3", "4"])
        hlayout.addWidget(options["lead"])

        snippet = CueSnippetButton(config, osc)
        hlayout.addWidget(snippet)
        options["snippet"] = snippet

        hlayout.addWidget(CueFireButton(config, osc, prevIndex, index, printIndex, widgets["cues"]))

        vlayout.addLayout(hlayout)
        widgets["cues"].append(options)

    widget = QWidget()
    widget.setLayout(vlayout)

    scroll = QScrollArea()
    scroll.setWidget(widget)
    scroll.setWidgetResizable(True)
    return scroll