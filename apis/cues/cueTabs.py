from apis.cues.cueFire import CueFireButton
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

class CueTab(QTabWidget):
    def __init__(self, config, osc, widgets):
        super().__init__()
        self.config = config
        self.osc = osc
        self.widgets = widgets
        self.prevIndex = [None]
        
        for i in range(0, self.config["cues"]["cuePages"]):
            self.addTab(CuesObject(config, osc, widgets, self.prevIndex, i), chr(97 + i))
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

class CuesObject(QScrollArea):
    def __init__(self, config, osc, widgets, prevIndex, pageIndex):
        super().__init__()
        self.buttons = []

        vlayout = QVBoxLayout()

        for cue in range(0, 10):
            index = (pageIndex * 10) + cue
            printIndex = str(cue + 1)
            options = {}

            hlayout = QHBoxLayout()

            options["label"] = QLabel(printIndex + ":")
            options["label"].setFixedWidth(20)
            hlayout.addWidget(options["label"])

            for category in config["cues"]["cueOptions"]:
                items = list(config["cues"]["cueOptions"][category].keys())
                try:
                    items.remove("RESET")
                except ValueError:
                    pass
                options[category] = QComboBox()
                options[category].setFixedWidth(120)
                options[category].setPlaceholderText(category)
                options[category].addItem("")
                options[category].addItems(items)
                hlayout.addWidget(options[category])

            snippet = CueSnippetButton(config, osc)
            hlayout.addWidget(snippet)
            options["snippet"] = snippet

            button = CueFireButton(config, osc, prevIndex, index, printIndex, widgets["cues"])
            hlayout.addWidget(button)
            self.buttons.append(button)

            vlayout.addLayout(hlayout)
            widgets["cues"].append(options)

        widget = QWidget()
        widget.setLayout(vlayout)

        self.setWidget(widget)
        self.setWidgetResizable(True)