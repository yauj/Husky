from apis.connection.connectionLayer import ConnectionLayer
from apis.cues.cueLayer import CueLayer
from apis.cues.cueLoad import loadCue
from apis.cues.cueSave import saveCue
from apis.menu.ClearCache import ClearCache
from apis.menu.UndoCommands import UndoCommands
from apis.menu.Update import UpdateApp
from apis.misc.miscLayer import MiscLayer
from apis.snippets.snippetsLayer import SnippetsLayer
from config import config
import faulthandler
import os
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QTabWidget,
)
import sys
from util.defaultOSC import MIDIVirtualPort

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.config = config
        self.widgets = {"connection": {}, "personal": {}, "tabs": {}, "cues": [], "faders": [], "routing": {}}
        self.osc = {}
        self.saveCache = True
        self.virtualPort = MIDIVirtualPort() # Virtual MIDI Port

        self.setWindowTitle("X32 Helper")

        self.loadConnectionCache()

        tabs = QTabWidget()

        tabs.addTab(ConnectionLayer(self.config, self.widgets, self.osc), "Connections")
        tabs.addTab(SnippetsLayer(self.config, self.widgets, self.osc), "Snippets")
        tabs.addTab(CueLayer(self.config, self.widgets, self.osc), "Cues")
        tabs.addTab(MiscLayer(self.config, self.widgets, self.osc), "Misc")

        self.loadCueCache()

        self.setCentralWidget(tabs)
        
        menu = self.menuBar().addMenu("&X32 Helper")
        prevCmdMenu = menu.addMenu("Undo Previous Commands")
        for mixerName in self.config["osc"]:
            prevCmdMenu.addAction(UndoCommands(self, self.osc, mixerName))
        menu.addAction(ClearCache(self))
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

            for name in self.config["midi"]:
                if name + "Midi" in connections:
                    self.config["midi"][name]["default"] = connections[name + "Midi"]

    # Load Cue Cache
    def loadCueCache(self):
        if os.path.exists("cue.cache"):
            with open("cue.cache") as file:
                loadCue(file, self.widgets)

    # Save Cache
    def closeEvent(self, a0):
        for mixerName in self.config["osc"]:
            self.osc[mixerName + "Server"].shutdown()
        self.osc["atemServer"].shutdown()

        if self.saveCache:
            with open("connection.cache", "w") as file:
                for param in self.widgets["connection"]:
                    file.write("\n" + param + " " + self.widgets["connection"][param].currentText())

            with open("cue.cache", "w") as file:
                saveCue(self.config, file, self.widgets)

        return super().closeEvent(a0)

faulthandler.enable()
app = QApplication(sys.argv)
window = MainWindow()
window.resize(599, 599)
window.show()
app.exec()