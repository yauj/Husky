import os
import sys

from apis.connection.connectMIDI import ConnectMidiButton
from apis.connection.connectOSC import ConnectOscButton
from apis.cues.cueLoad import CueLoadButton
from apis.cues.cueSave import CueSaveButton
from apis.cues.cueTabs import CueTab
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
from util.defaultOSC import MIDIServer, RetryingServer
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
        self.osc = {
            "server": RetryingServer(),
            "serverMidi": MIDIServer()
        }

        self.setWindowTitle("X32 Helper")

        tabs = QTabWidget()

        tabs.addTab(self.connectionLayer(), "X32 Connection")
        tabs.addTab(self.snippetsLayer(), "Snippets")
        tabs.addTab(self.cuesLayer(), "Cues")
        tabs.addTab(self.tracksLayer(), "Tracks")
        tabs.addTab(self.transferLayer(), "FOH->IEM")
        
        self.setCentralWidget(tabs)
        
        menu = self.menuBar().addMenu("&X32 Helper")
        menu.addAction(UpdateApp(self))
    
    def connectionLayer(self):
        vlayout = QVBoxLayout()

        validIps = self.osc["server"].getAvailableIPs()

        for mixerName in config["osc"]:
            hlayout = QHBoxLayout()

            label = QLabel(mixerName.upper() + " Mixer IP Address:")
            label.setFixedWidth(150)
            hlayout.addWidget(label)

            address = QComboBox()
            address.setEditable(True)
            address.addItems(validIps)
            address.setCurrentText(config["osc"][mixerName])
            address.setFixedWidth(300)
            hlayout.addWidget(address)

            status = QLabel()
            hlayout.addWidget(status)
            
            hlayout.addWidget(ConnectOscButton(self.osc, address, status, mixerName))

            vlayout.addLayout(hlayout)
        
        for name in config["midi"]:
            hlayout = QHBoxLayout()
            label = QLabel(name.capitalize() + " MIDI: ")
            label.setFixedWidth(150)
            hlayout.addWidget(label)

            port = QComboBox()
            port.setEditable(True)
            port.setFixedWidth(300)
            port.setCurrentText(config["midi"][name])
            hlayout.addWidget(port)

            status = QLabel()
            hlayout.addWidget(status)

            hlayout.addWidget(ConnectMidiButton(self.osc, name, status, port))

            port.addItems(self.osc[name + "Midi"].get_output_names())
            port.setCurrentText(config["midi"][name])

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

        tabs = CueTab(self.osc, self.widgets)

        hlayout = QHBoxLayout()
        hlayout.addWidget(CueLoadButton(tabs.getCues()))
        hlayout.addWidget(CueSaveButton(tabs.getCues()))
        vlayout.addLayout(hlayout)

        vlayout.addWidget(QLabel("Fire Cues. Green indicates last cue fired was successful. Red indicates failure."))

        vlayout.addWidget(tabs)

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
        for letter in self.widgets["cue"]:
            page.addItem(letter)
        hlayout.addWidget(page)

        cue = QComboBox()
        cue.setPlaceholderText("Index")
        for index in self.widgets["cue"][letter]:
            cue.addItem(index)
        hlayout.addWidget(cue)

        vlayout.addLayout(hlayout)
   
        options = {
            "personal": {},
            "settings": {}
        }

        for chName in config["personal"]:
            hlayout = QHBoxLayout()

            hlayout.addWidget(QLabel(chName + ":"))

            options["personal"][chName] = {}

            hlayout.addWidget(QLabel("FOH"))
            if "channels" in config["personal"][chName]:
                options["personal"][chName]["channels"] = QCheckBox()
                hlayout.addWidget(options["personal"][chName]["channels"])
            else:
                hlayout.addWidget(QLabel("-"))

            hlayout.addWidget(QLabel("IEM"))
            if "iem_bus" in config["personal"][chName]:
                options["personal"][chName]["iem_bus"] = QCheckBox()
                hlayout.addWidget(options["personal"][chName]["iem_bus"])
            else:
                hlayout.addWidget(QLabel("-"))
            
            vlayout.addLayout(hlayout)

        for setting in config["settings"]:
            hlayout = QHBoxLayout()

            hlayout.addWidget(QLabel(setting + ":"))
            options["settings"][setting] = QCheckBox()
            hlayout.addWidget(options["settings"][setting])

            vlayout.addLayout(hlayout)
        
        vlayout.addWidget(SnippetSaveButton(self.widgets, self.osc, config, options, page, cue))

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
        vlayout.addWidget(TransferButton(self.widgets, self.osc))

        widget = QWidget()
        widget.setLayout(vlayout)
        return widget

app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()