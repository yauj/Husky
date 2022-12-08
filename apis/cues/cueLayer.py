import sys

from apis.cues.faders.fadersTab import FaderTab
sys.path.insert(0, '../')

from apis.cues.cueLoad import CueLoadButton
from apis.cues.cueSave import CueSaveButton
from apis.cues.cueTabs import CueTab
from apis.cues.snippet.snippetAdd import SnippetAddButton
from apis.cues.snippet.snippetEdit import SnippetEditButton
from apis.cues.snippet.snippetFire import SnippetFireButton
from apis.cues.snippet.snippetLoad import SnippetLoadButton
from apis.cues.snippet.snippetSave import SnippetSaveButton
from apis.cues.snippet.snippetUpdate import SnippetUpdateButton
from PyQt6.QtWidgets import (
    QCheckBox,
    QComboBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QTabWidget,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

class CueLayer(QTabWidget):
    def __init__(self, config, widgets, osc):
        super().__init__()
        self.config = config
        self.widgets = widgets
        self.osc = osc

        self.addTab(self.mainLayer(), "Main")
        self.addTab(self.snippetLayer(), "Snippet")

    def mainLayer(self):
        vlayout = QVBoxLayout()

        tabs = CueTab(self.osc, self.widgets)
        faders = FaderTab(self.config, self.widgets, self.osc)

        hlayout = QHBoxLayout()
        hlayout.addWidget(CueLoadButton(self.widgets))
        hlayout.addWidget(CueSaveButton(self.widgets))
        vlayout.addLayout(hlayout)

        vlayout.addWidget(QLabel("Fire Cues. Green indicates last cue fired was successful. Red indicates failure."))

        subLayer = QTabWidget()
        subLayer.addTab(tabs, "Cues")
        subLayer.addTab(faders, "Faders")

        vlayout.addWidget(subLayer)

        widget = QWidget()
        widget.setLayout(vlayout)
        return widget

    def snippetLayer(self):
        tabs = QTabWidget()

        tabs.addTab(self.snippetSaveLayer(), "Save")
        tabs.addTab(self.snippetEditLayer(), "Edit")

        return tabs

    def snippetSaveLayer(self):
        vlayout = QVBoxLayout()

        vlayout.addWidget(QLabel("Save new Snippet to be fired by Cue"))

        hlayout = QHBoxLayout()

        hlayout.addWidget(QLabel("Cue: "))

        page = QComboBox()
        page.setPlaceholderText("Page")
        for letter in self.widgets["cueSnippet"]:
            page.addItem(letter)
        hlayout.addWidget(page)

        cue = QComboBox()
        cue.setPlaceholderText("Index")
        for index in self.widgets["cueSnippet"][letter]:
            cue.addItem(index)
        hlayout.addWidget(cue)

        vlayout.addLayout(hlayout)
   
        options = {
            "personal": {},
            "settings": {}
        }

        for chName in self.config["personal"]:
            hlayout = QHBoxLayout()

            hlayout.addWidget(QLabel(chName + ":"))

            options["personal"][chName] = {}

            hlayout.addWidget(QLabel("FOH"))
            if "channels" in self.config["personal"][chName]:
                options["personal"][chName]["channels"] = QCheckBox()
                hlayout.addWidget(options["personal"][chName]["channels"])
            else:
                hlayout.addWidget(QLabel("-"))

            hlayout.addWidget(QLabel("IEM"))
            if "iem_bus" in self.config["personal"][chName]:
                options["personal"][chName]["iem_bus"] = QCheckBox()
                hlayout.addWidget(options["personal"][chName]["iem_bus"])
            else:
                hlayout.addWidget(QLabel("-"))
            
            vlayout.addLayout(hlayout)

        for setting in self.config["settings"]:
            hlayout = QHBoxLayout()

            hlayout.addWidget(QLabel(setting + ":"))
            options["settings"][setting] = QCheckBox()
            hlayout.addWidget(options["settings"][setting])

            vlayout.addLayout(hlayout)
        
        vlayout.addWidget(SnippetSaveButton(self.widgets, self.osc, self.config, options, page, cue))

        widget = QWidget()
        widget.setLayout(vlayout)
        return widget
    
    def snippetEditLayer(self):
        vlayout = QVBoxLayout()

        vlayout.addWidget(QLabel("Modify existing snippet"))
        
        hlayout = QHBoxLayout()
        hlayout.addWidget(QLabel("Filename: "))
        filename = QLineEdit()
        filename.setReadOnly(True)
        hlayout.addWidget(filename)
        vlayout.addLayout(hlayout)

        textbox = QTextEdit()
        vlayout.addWidget(textbox)

        hlayout = QHBoxLayout()
        hlayout.addWidget(SnippetAddButton(self.osc, textbox))
        hlayout.addWidget(SnippetUpdateButton(self.osc, textbox))
        hlayout.addWidget(SnippetFireButton(self.osc, textbox))
        vlayout.addLayout(hlayout)

        hlayout = QHBoxLayout()
        hlayout.addWidget(SnippetLoadButton(filename, textbox))
        hlayout.addWidget(SnippetEditButton(filename, textbox))
        vlayout.addLayout(hlayout)

        widget = QWidget()
        widget.setLayout(vlayout)
        return widget