import os
import sys

import mido
from apis.connection.connect import ConnectButton

from apis.cues.cueFire import CueFireButton
from apis.cues.cueLoad import CueLoadButton
from apis.cues.cueSave import CueSaveButton
from apis.cues.snippet.snippetEdit import SnippetEditButton
from apis.cues.snippet.snippetLoad import SnippetLoadButton
from apis.cues.snippet.snippetSave import SnippetSaveButton
from apis.snippets.loadAll import LoadAllButton
from apis.snippets.loadSingle import LoadButton
from apis.snippets.saveAll import SaveAllButton
from apis.snippets.saveSingle import SaveButton
from apis.tracks.tracksSlider import TracksSlider
from apis.transfer.transferSettings import TransferButton
from config import config
from util.constants import KEYS, MIDI_BUS
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
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.widgets = {"personal": {}, "cue": {}}
        server = RetryingServer()
        self.osc = {
            "server": server,
            "midi": mido.Backend("mido.backends.rtmidi").open_output(MIDI_BUS)
        }

        self.setWindowTitle("X32 Helper")

        tabs = QTabWidget()

        tabs.addTab(self.connectionLayer(), "X32 Connection")
        tabs.addTab(self.snippetsLayer(), "Snippets")
        tabs.addTab(self.cuesLayer(), "Cues")
        tabs.addTab(self.tracksLayer(), "Tracks")
        tabs.addTab(self.transferLayer(), "FOH->IEM")
        
        self.setCentralWidget(tabs)
    
    def connectionLayer(self):
        vlayout = QVBoxLayout()

        for mixerName in config["ip"]:
            hlayout = QHBoxLayout()

            hlayout.addWidget(QLabel(mixerName.upper() + " Mixer IP Address:"))

            address = QLineEdit(config["ip"][mixerName])
            hlayout.addWidget(address)

            status = QLabel()
            hlayout.addWidget(status)
            
            hlayout.addWidget(ConnectButton(self.osc, address, status, mixerName))

            vlayout.addLayout(hlayout)

        widget = QWidget()
        widget.setLayout(vlayout)
        return widget

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

            hlayout.addWidget(LoadButton(self.widgets, self.osc, chName, filenames[chName], self.widgets["personal"][chName]))

            vlayout.addLayout(hlayout)
        
        vlayout.addWidget(LoadAllButton(self.widgets, self.osc, filenames, self.widgets["personal"]))

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

            hlayout.addWidget(SaveButton(self.widgets, self.osc, chName, self.widgets["personal"][chName], config["personal"][chName]))

            vlayout.addLayout(hlayout)

        vlayout.addWidget(SaveAllButton(self.widgets, self.osc, self.widgets["personal"], config["personal"]))

        widget = QWidget()
        widget.setLayout(vlayout)
        return widget
    
    def cuesLayer(self):
        tabs = QTabWidget()

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

            hlayout.addWidget(CueFireButton(self.widgets, self.osc, index, options))

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
        tabs = QTabWidget()

        tabs.addTab(self.snippetSaveLayer(), "Save")
        tabs.addTab(self.snippetEditLayer(), "Edit")

        return tabs

    def snippetSaveLayer(self):
        vlayout = QVBoxLayout()

        vlayout.addWidget(QLabel("Save new Snippet to be fired by Cue"))

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
        
        vlayout.addWidget(SnippetSaveButton(self.widgets, self.osc, config["personal"], options, cue))

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
        hlayout.addWidget(SnippetLoadButton(filename, textbox))
        hlayout.addWidget(SnippetEditButton(filename, textbox))
        vlayout.addLayout(hlayout)

        widget = QWidget()
        widget.setLayout(vlayout)
        return widget

    def tracksLayer(self):
        vlayout = QVBoxLayout()

        vlayout.addWidget(QLabel("Volume Sliders for tracks"))

        hlayout = QHBoxLayout()

        sliders = ["BGVS", "Choir", "Keys", "EG", "Bass", "Drums"]

        for i in range (0, len(sliders)):
            sliderLayout = QVBoxLayout()

            sliderLayout.addWidget(TracksSlider(self.osc, i + 50))
            sliderLayout.addWidget(QLabel(sliders[i]))

            hlayout.addLayout(sliderLayout)

        vlayout.addLayout(hlayout)

        widget = QWidget()
        widget.setLayout(vlayout)
        return widget

    def transferLayer(self):
        vlayout = QVBoxLayout()

        vlayout.addWidget(QLabel("Do you want to transfer Channel EQ, Compression, Mute settings from the FOH Mixer to the IEM Mixer?"))
        vlayout.addWidget(TransferButton(self.widgets, self.osc))

        widget = QWidget()
        widget.setLayout(vlayout)
        return widget

app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()