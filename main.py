from apis.connection.connectionLayer import ConnectionLayer
from apis.connection.listenMIDI import loadMidi, saveMidi
from apis.cues.cueLayer import CueLayer
from apis.cues.cueLoad import loadCue
from apis.cues.cueSave import saveCue
from apis.menu.About import About
from apis.menu.ClearCache import ClearCache
from apis.menu.UndoCommands import UndoCommands
from apis.menu.Update import UpdateApp
from apis.misc.miscLayer import MiscLayer
from apis.snippets.snippetsLayer import SnippetsLayer
from config import config
from datetime import datetime
import faulthandler
import logging
import os
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QTabWidget,
)
import sys
import traceback
from util.constants import APP_NAME
from util.defaultOSC import MIDIServer, MIDIVirtualPort

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.config = config
        self.widgets = {"connection": {}, "personal": {}, "tabs": {}, "cues": [], "faders": [], "routing": {}}
        self.osc = {}
        self.saveCache = True
        self.virtualPort = MIDIVirtualPort() # Virtual MIDI Port

        self.setWindowTitle(APP_NAME)

        self.loadConnectionCache()

        tabs = QTabWidget()

        tabs.addTab(ConnectionLayer(self.config, self.widgets, self.osc), "Connections")
        tabs.addTab(SnippetsLayer(self.config, self.widgets, self.osc), "Snippets")
        tabs.addTab(CueLayer(self.config, self.widgets, self.osc), "Cues")
        tabs.addTab(MiscLayer(self.config, self.widgets, self.osc), "Misc")

        self.loadCueCache()

        self.setCentralWidget(tabs)
        
        menu = self.menuBar().addMenu("&Menu")
        menu.addAction(About(self))
        prevCmdMenu = menu.addMenu("Undo Previous Commands")
        for mixerName in self.config["osc"]:
            prevCmdMenu.addAction(UndoCommands(self, self.osc, mixerName))
        menu.addAction(ClearCache(self))
        menu.addAction(UpdateApp(self))
    
    # Load Connection Cache
    def loadConnectionCache(self):
        if os.path.exists("data/connection.cache"):
            connections = {}
            with open("data/connection.cache") as file:
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
            
        if os.path.exists("data/serverMidi.cache"):
            with open("data/serverMidi.cache") as file:
                loadMidi(file, self.osc, self.widgets)
        else:
            # Load Default
            self.osc["serverMidi"] = {}
            for portName in config["serverMidi"]:
                self.osc["serverMidi"][portName] = MIDIServer(portName, self.widgets)
                for param in config["serverMidi"][portName]:
                    self.osc["serverMidi"][portName].addCallback(param)
                self.osc["serverMidi"][portName].open_ioPort()

    # Load Cue Cache
    def loadCueCache(self):
        if os.path.exists("data/cue.cache"):
            with open("data/cue.cache") as file:
                loadCue(file, self.widgets)

    # Save Cache
    def closeEvent(self, a0):
        for mixerName in self.config["osc"]:
            self.osc[mixerName + "Server"].shutdown()
        self.osc["atemServer"].shutdown()

        if self.saveCache:
            with open("data/connection.cache", "w") as file:
                file.write("v1.0")
                for param in self.widgets["connection"]:
                    file.write("\n" + param + " " + self.widgets["connection"][param].currentText())

            with open("data/serverMidi.cache", "w") as file:
                saveMidi(file, self.osc)

            with open("data/cue.cache", "w") as file:
                saveCue(self.config, file, self.widgets)

        return super().closeEvent(a0)

def excepthook(exc_type, exc_value, exc_tb):
    tb = "".join(traceback.format_exception(exc_type, exc_value, exc_tb))
    logging.getLogger("SYSERRR").critical(tb)
    QApplication.quit()
    logFile.close()
    # Copy Log file to tmp directory (Might be too Mac dependent)
    os.system("cp data/app.log ~/Library/Logs/" + APP_NAME + "-crash-" + datetime.now().strftime('%Y%m%d%H%M%S') + ".log")

os.chdir(os.path.dirname(__file__))
if not os.path.exists("pyinstaller.sh"): # Not in Main Directory
    os.chdir("../Resources")
logFile = open("data/app.log", "w")
sys.excepthook = excepthook
faulthandler.enable(logFile)
logging.basicConfig(stream = logFile, level = logging.INFO, format = "%(asctime)s\t|%(levelname)s\t|%(name)s\t|%(message)s")
logger = logging.getLogger(__name__)
app = QApplication(sys.argv)
window = MainWindow()
window.resize(599, 599)
window.show()
app.exec()
logFile.close()