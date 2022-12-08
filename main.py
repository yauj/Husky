import os
import sys

from apis.connection.connectMIDI import ConnectMidiButton
from apis.connection.connectOSC import ConnectOscButton
from apis.connection.listenMIDI import ListenMidiButton
from apis.cues.cueLoad import CueLoadButton, loadCue
from apis.cues.cueSave import CueSaveButton, saveCue
from apis.cues.cueTabs import CueTab
from apis.cues.faders.fadersEdit import FadersEditButton
from apis.cues.faders.fadersSlider import FadersSlider
from apis.cues.snippet.snippetAdd import SnippetAddButton
from apis.cues.snippet.snippetEdit import SnippetEditButton
from apis.cues.snippet.snippetFire import SnippetFireButton
from apis.cues.snippet.snippetLoad import SnippetLoadButton
from apis.cues.snippet.snippetSave import SnippetSaveButton
from apis.cues.snippet.snippetUpdate import SnippetUpdateButton
from apis.menu.Update import UpdateApp
from apis.snippets.loadAll import LoadAllButton
from apis.snippets.loadSingle import LoadButton
from apis.snippets.saveAll import SaveAllButton
from apis.snippets.saveSingle import SaveButton
from apis.tracks.tracksSlider import TracksSlider
from apis.transfer.transferSettings import TransferButton
from config import config
from util.defaultOSC import AvailableIPs, MIDIVirtualPort, RetryingServer
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

        self.config = config
        self.widgets = {"connection": {}, "personal": {}, "cues": [], "cueSnippet": {}, "faders": []}
        self.osc = {}
        self.server = RetryingServer() # Server used for generic calls
        self.virtualPort = MIDIVirtualPort() # Virtual MIDI Port

        self.setWindowTitle("X32 Helper")

        self.loadConnectionCache()

        tabs = QTabWidget()

        tabs.addTab(self.connectionLayer(), "X32 Connection")
        tabs.addTab(self.snippetsLayer(), "Snippets")
        tabs.addTab(self.cuesLayer(), "Cues")
        tabs.addTab(self.tracksLayer(), "Tracks")
        tabs.addTab(self.transferLayer(), "FOH->IEM")

        self.loadCueCache()

        self.setCentralWidget(tabs)
        
        menu = self.menuBar().addMenu("&X32 Helper")
        menu.addAction(UpdateApp(self))
    
    def connectionLayer(self):
        vlayout = QVBoxLayout()

        validIPs = AvailableIPs().get()

        for mixerName in self.config["osc"]:
            hlayout = QHBoxLayout()

            label = QLabel(mixerName.upper() + " Mixer IP Address:")
            label.setFixedWidth(150)
            hlayout.addWidget(label)

            address = QComboBox()
            address.setEditable(True)
            address.addItems(validIPs)
            address.setCurrentText(self.config["osc"][mixerName])
            address.setFixedWidth(300)
            self.widgets["connection"][mixerName + "Client"] = address
            hlayout.addWidget(address)

            status = QLabel()
            hlayout.addWidget(status)
            
            hlayout.addWidget(ConnectOscButton(self.osc, address, status, mixerName, self.server))

            vlayout.addLayout(hlayout)

        hlayout = QHBoxLayout()
        label = QLabel("MIDI Input: ")
        label.setFixedWidth(150)
        hlayout.addWidget(label)

        port = QComboBox()
        port.setEditable(True)
        port.setFixedWidth(300)
        port.setCurrentText(self.config["serverMidi"])
        self.widgets["connection"]["serverMidi"] = port
        hlayout.addWidget(port)

        status = QLabel()
        hlayout.addWidget(status)

        hlayout.addWidget(ListenMidiButton(self.osc, status, port))

        port.addItems(self.osc["serverMidi"].get_input_names())
        port.setCurrentText(self.config["serverMidi"])

        vlayout.addLayout(hlayout)
        
        for name in self.config["midi"]:
            hlayout = QHBoxLayout()
            label = QLabel(name.capitalize() + " MIDI: ")
            label.setFixedWidth(150)
            hlayout.addWidget(label)

            port = QComboBox()
            port.setEditable(True)
            port.setFixedWidth(300)
            port.setCurrentText(self.config["midi"][name])
            self.widgets["connection"][name + "Midi"] = port
            hlayout.addWidget(port)

            status = QLabel()
            hlayout.addWidget(status)

            hlayout.addWidget(ConnectMidiButton(self.osc, name, status, port))

            port.addItems(self.osc[name + "Midi"].get_output_names())
            port.setCurrentText(self.config["midi"][name])

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

        for chName in self.config["personal"]:
            hlayout = QHBoxLayout()

            hlayout.addWidget(QLabel(chName + ":"))

            files = []
            for filename in os.listdir("data"):
                try:
                    if filename.split(".")[0].split("_")[1] == chName:
                        files.append(filename)
                except IndexError:
                    pass
            files.sort(reverse=True)

            filenames[chName] = QComboBox()
            filenames[chName].addItems(files)
            filenames[chName].setEditable(True)
            filenames[chName].setMaxCount(10)
            filenames[chName].setFixedWidth(300)
            filenames[chName].setCurrentIndex(-1)
            hlayout.addWidget(filenames[chName])

            hlayout.addWidget(LoadButton(self.osc, chName, filenames[chName], self.widgets["personal"][chName]))

            vlayout.addLayout(hlayout)
        
        vlayout.addWidget(LoadAllButton(self.osc, filenames, self.widgets["personal"]))

        widget = QWidget()
        widget.setLayout(vlayout)
        return widget

    def snippetsSaveLayer(self):
        vlayout = QVBoxLayout()

        vlayout.addWidget(QLabel("Enter name of person in textbox in the following format: 'FirstnameLastname'."))
        vlayout.addWidget(QLabel("Leave textbox blank if you don't want to save."))

        for chName in self.config["personal"]:
            hlayout = QHBoxLayout()

            hlayout.addWidget(QLabel(chName + ":"))

            names = []
            for filename in os.listdir("data"):
                try:
                    components = filename.split(".")[0].split("_")
                    if components[1] == chName:
                        names.append(components[2])
                except IndexError:
                    pass
            names = list(set(names))
            names.sort()

            self.widgets["personal"][chName] = QComboBox()
            self.widgets["personal"][chName].addItems(names)
            self.widgets["personal"][chName].setEditable(True)
            self.widgets["personal"][chName].setMaxCount(10)
            self.widgets["personal"][chName].setFixedWidth(300)
            self.widgets["personal"][chName].setCurrentIndex(-1)
            hlayout.addWidget(self.widgets["personal"][chName])

            hlayout.addWidget(SaveButton(self.osc, chName, self.widgets["personal"][chName], self.config["personal"][chName]))

            vlayout.addLayout(hlayout)

        vlayout.addWidget(SaveAllButton(self.osc, self.widgets["personal"], self.config["personal"]))

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

        tabs = CueTab(self.osc, self.widgets)
        faders = self.cuesFadersLayer()

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
    
    def cuesFadersLayer(self):
        vlayout = QVBoxLayout()

        vlayout.addWidget(QLabel("Volume Sliders for tracks"))

        hlayout = QHBoxLayout()

        for i, name in enumerate(self.config["faders"]):
            fader = {}
            fader["commands"] = self.config["faders"][name]

            sliderLayout = QVBoxLayout()

            fader["name"] = QLineEdit(name)

            sliderLayout.addWidget(FadersSlider(self.osc, fader, i))
            sliderLayout.addWidget(fader["name"])
            sliderLayout.addWidget(FadersEditButton(self.osc, fader))

            self.widgets["faders"].append(fader)
            hlayout.addLayout(sliderLayout)

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
        vlayout.addWidget(TransferButton(self.osc))

        widget = QWidget()
        widget.setLayout(vlayout)
        return widget
    
    # Load Connection Cache
    def loadConnectionCache(self):
        if os.path.exists("connection.cache"):
            connections = {}
            with open("connection.cache") as file:
                file.readline() # Skip Header Line
                while (line := file.readline().strip()):
                    components = line.split()
                    connections[components[0]] = " ".join(components[1:])
            
            for mixerName in self.config["osc"]:
                if mixerName + "Client" in connections:
                    self.config["osc"][mixerName] = connections[mixerName + "Client"]

            if "serverMidi" in connections:
                self.config["serverMidi"] = connections["serverMidi"]

            for name in self.config["midi"]:
                if name + "Midi" in connections:
                    self.config["midi"][name] = connections[name + "Midi"]

    # Load Cue Cache
    def loadCueCache(self):
        if os.path.exists("cue.cache"):
            with open("cue.cache") as file:
                loadCue(file, self.widgets)

    # Save Cache
    def closeEvent(self, a0):
        with open("connection.cache", "w") as file:
            for param in self.widgets["connection"]:
                file.write("\n" + param + " " + self.widgets["connection"][param].currentText())

        with open("cue.cache", "w") as file:
            saveCue(file, self.widgets)

        return super().closeEvent(a0)

app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()