from apis.connection.connectionLayer import ConnectionLayer
from apis.cues.cueLayer import CueLayer
from apis.cues.cueLoad import loadCue
from apis.cues.cueSave import saveCue
from apis.menu.Update import UpdateApp
from apis.misc.miscLayer import MiscLayer
from apis.snippets.snippetsLayer import SnippetsLayer
from config import config
import os
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QTabWidget,
)
import sys
from util.defaultOSC import MIDIVirtualPort, RetryingServer

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.config = config
        self.widgets = {"connection": {}, "personal": {}, "cues": [], "cueSnippet": {}, "faders": [], "routing": {}, "routingSwap": {}}
        for mixerName in self.config["osc"]:
            self.widgets["routing"][mixerName] = {}
        self.osc = {}
        self.server = RetryingServer() # Server used for generic calls
        self.virtualPort = MIDIVirtualPort() # Virtual MIDI Port

        self.setWindowTitle("X32 Helper")

        self.loadConnectionCache()

        tabs = QTabWidget()

        tabs.addTab(ConnectionLayer(self.config, self.widgets, self.osc, self.server), "X32 Connection")
        tabs.addTab(SnippetsLayer(self.config, self.widgets, self.osc), "Snippets")
        tabs.addTab(CueLayer(self.config, self.widgets, self.osc), "Cues")
        tabs.addTab(MiscLayer(self.config, self.widgets, self.osc), "Misc")

        self.loadCueCache()

        self.setCentralWidget(tabs)
        
        menu = self.menuBar().addMenu("&X32 Helper")
        menu.addAction(UpdateApp(self))
    
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
window.resize(1, 1) # Open in smallest size
window.show()
app.exec()