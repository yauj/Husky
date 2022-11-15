import os
import sys

from apis.cues.cueFire import CueFireButton
from apis.cues.cueLoad import CueLoadButton
from apis.cues.cueSave import CueSaveButton
from apis.cues.cueSnippet import CueSnippetButton
from apis.snippets.loadAll import LoadAllButton
from apis.snippets.loadSingle import LoadButton
from apis.snippets.saveAll import SaveAllButton
from apis.snippets.saveSingle import SaveButton
from apis.transfer.transferSettings import TransferButton
from config import config
from util.constants import KEYS
from util.defaultOSC import RetryingServer
from PyQt6.QtWidgets import (
    QApplication,
    QCheckBox,
    QComboBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QTabWidget,
    QVBoxLayout,
    QWidget,
)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.widgets = {"personal": {}, "ip": {}, "cue": {}}
        self.server = RetryingServer()

        self.setWindowTitle("X32 Helper")

        tabs = QTabWidget()

        tabs.addTab(self.snippetsLayer(), "Snippets")
        tabs.addTab(self.cuesLayer(), "Cues")
        tabs.addTab(self.transferLayer(), "FOH->IEM")
        tabs.addTab(self.prefLayer(), "Preferences")
        
        self.setCentralWidget(tabs)

    def snippetsLayer(self):
        tabs = QTabWidget()

        # Need to compile saveLayer first, since loadLayer is dependent on saveLayer
        saveLayer = self.snippetsSaveLayer()
        loadLayer = self.snippetsLoadLayer()

        tabs.addTab(loadLayer, "Load")
        tabs.addTab(saveLayer, "Save")

        return tabs

    def snippetsLoadLayer(self):
        vlayout = QVBoxLayout()

        vlayout.addWidget(QLabel("Enter filename in textbox."))
        vlayout.addWidget(QLabel("Leave textbox blank if you don't want to load."))

        filenames = {}

        for chName in config["personal"]:
            hlayout = QHBoxLayout()

            hlayout.addWidget(QLabel(chName + ":"))

            files = []
            for filename in os.listdir("data"):
                if filename.split(".")[0].split("_")[1] == chName:
                    files.append(filename)
            files.sort(reverse=True)

            filenames[chName] = QComboBox()
            filenames[chName].addItems(files)
            filenames[chName].setEditable(True)
            filenames[chName].setMaxCount(10)
            filenames[chName].setFixedWidth(300)
            filenames[chName].setCurrentIndex(-1)
            hlayout.addWidget(filenames[chName])

            hlayout.addWidget(LoadButton(self.widgets, self.server, chName, filenames[chName], self.widgets["personal"][chName]))

            vlayout.addLayout(hlayout)
        
        vlayout.addWidget(LoadAllButton(self.widgets, self.server, filenames, self.widgets["personal"]))

        widget = QWidget()
        widget.setLayout(vlayout)
        return widget


    def snippetsSaveLayer(self):
        vlayout = QVBoxLayout()

        vlayout.addWidget(QLabel("Enter name of person in textbox in the following format: 'FirstnameLastname'."))
        vlayout.addWidget(QLabel("Leave textbox blank if you don't want to save."))

        for chName in config["personal"]:
            hlayout = QHBoxLayout()

            hlayout.addWidget(QLabel(chName + ":"))

            names = []
            for filename in os.listdir("data"):
                components = filename.split(".")[0].split("_")
                if components[1] == chName:
                    names.append(components[2])
            names = list(set(names))
            names.sort()

            self.widgets["personal"][chName] = QComboBox()
            self.widgets["personal"][chName].addItems(names)
            self.widgets["personal"][chName].setEditable(True)
            self.widgets["personal"][chName].setMaxCount(10)
            self.widgets["personal"][chName].setFixedWidth(300)
            self.widgets["personal"][chName].setCurrentIndex(-1)
            hlayout.addWidget(self.widgets["personal"][chName])

            hlayout.addWidget(SaveButton(self.widgets, self.server, chName, self.widgets["personal"][chName], config["personal"][chName]))

            vlayout.addLayout(hlayout)

        vlayout.addWidget(SaveAllButton(self.widgets, self.server, self.widgets["personal"], config["personal"]))

        widget = QWidget()
        widget.setLayout(vlayout)
        return widget
    
    def cuesLayer(self):
        tabs = QTabWidget()

        # Need to compile saveLayer first, since loadLayer is dependent on saveLayer

        tabs.addTab(self.cuesMainLayer(), "Main")
        tabs.addTab(self.cuesSnippetLayer(), "Snippet")

        return tabs

    def cuesMainLayer(self):
        vlayout = QVBoxLayout()

        vlayout.addWidget(QLabel("Fire cues per song"))

        cues = []

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
            self.widgets["cue"][index] = snippet

            hlayout.addWidget(CueFireButton(self.widgets, self.server, index, options))

            vlayout.addLayout(hlayout)
            cues.append(options)

        hlayout = QHBoxLayout()
        
        hlayout.addWidget(CueLoadButton(cues))
        hlayout.addWidget(CueSaveButton(cues))

        vlayout.addLayout(hlayout)

        widget = QWidget()
        widget.setLayout(vlayout)
        return widget

    def cuesSnippetLayer(self):
        vlayout = QVBoxLayout()

        vlayout.addWidget(QLabel("Save Snippet to be loaded by cue"))

        hlayout = QHBoxLayout()

        hlayout.addWidget(QLabel("Cue: "))

        cue = QComboBox()
        cue.setPlaceholderText("Index")
        for index in self.widgets["cue"]:
            cue.addItem(index)
        hlayout.addWidget(cue)

        vlayout.addLayout(hlayout)
   
        options = {}

        for chName in config["personal"]:
            hlayout = QHBoxLayout()

            hlayout.addWidget(QLabel(chName + ":"))

            options[chName] = {}

            hlayout.addWidget(QLabel("FOH"))
            if "channels" in config["personal"][chName]:
                options[chName]["channels"] = QCheckBox()
                hlayout.addWidget(options[chName]["channels"])
            else:
                hlayout.addWidget(QLabel("-"))

            hlayout.addWidget(QLabel("IEM"))
            if "iem_bus" in config["personal"][chName]:
                options[chName]["iem_bus"] = QCheckBox()
                hlayout.addWidget(options[chName]["iem_bus"])
            else:
                hlayout.addWidget(QLabel("-"))
            
            vlayout.addLayout(hlayout)
        
        vlayout.addWidget(CueSnippetButton(self.widgets, self.server, config["personal"], options, cue))

        widget = QWidget()
        widget.setLayout(vlayout)
        return widget


    def transferLayer(self):
        vlayout = QVBoxLayout()

        vlayout.addWidget(QLabel("Are you sure you want to transfer EQ, Compression settings to the IEM Mixer?"))
        vlayout.addWidget(TransferButton(self.widgets, self.server))

        widget = QWidget()
        widget.setLayout(vlayout)
        return widget

    def prefLayer(self):
        vlayout = QVBoxLayout()

        for mixerName in config["ip"]:
            hlayout = QHBoxLayout()

            hlayout.addWidget(QLabel(mixerName + " Mixer IP Address:"))

            self.widgets["ip"][mixerName] = QLineEdit(config["ip"][mixerName])
            hlayout.addWidget(self.widgets["ip"][mixerName])

            vlayout.addLayout(hlayout)

        widget = QWidget()
        widget.setLayout(vlayout)
        return widget

app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()