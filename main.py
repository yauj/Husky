import mido
from apis.connection.connectionLayer import ConnectionLayer
from apis.cues.cueLayer import CueLayer
from apis.cues.cueLoad import loadCue
from apis.cues.cueSave import saveCue
from apis.menu.About import About
from apis.menu.CopyChannels import CopyChannels
from apis.menu.Preferences import Preferences
from apis.menu.ResetCache import ResetCache
from apis.menu.ResetCommands import ResetCommands
from apis.menu.SwapChannels import SwapChannels
from apis.menu.SyncDirectory import BackupDirectory, LoadDirectory
from apis.menu.TransferSettings import TransferButton
from apis.menu.UndoCommands import UndoCommands
from apis.menu.Update import UpdateApp
from apis.pages.pagesLayer import PagesLayer
from apis.snippets.snippetsLayer import SnippetsLayer
from config import config
from datetime import datetime
import faulthandler
import json
import logging
import os
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QTabWidget,
)
import subprocess
import sys
import traceback
from util.constants import APP_NAME, SELECT_STAT, TALKBACK_STAT_PREFIX
from util.defaultOSC import MIDIVirtualPort

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.config = config
        self.widgets = {"connection": {}, "personal": {}, "tabs": {}, "cues": [], "faders": [], "routing": {}, "windows": {}}
        self.osc = {
            "virtualMidi": MIDIVirtualPort() # Virtual MIDI Port
        }
        self.saveCache = True

        self.setWindowTitle(APP_NAME)

        self.loadConfigCache()

        tabs = QTabWidget()

        tabs.addTab(ConnectionLayer(self.config, self.widgets, self.osc), "Connections")
        tabs.addTab(SnippetsLayer(self.config, self.widgets, self.osc), "Snippets")
        tabs.addTab(CueLayer(self.config, self.widgets, self.osc), "Cues")
        tabs.addTab(PagesLayer(self.config, self.widgets, self.osc), "Pages")

        self.loadCueCache()

        self.setCentralWidget(tabs)
        
        menu = self.menuBar().addMenu("&Menu")
        menu.addAction(About(self))
        menu.addAction(Preferences(self))
        prevCmdMenu = menu.addMenu("Undo Previous Commands")
        for mixerName in self.config["osc"]:
            prevCmdMenu.addAction(UndoCommands(self, self.osc, mixerName))
        prevCmdMenu = menu.addMenu("Sync App Directory")
        prevCmdMenu.addAction(BackupDirectory(self))
        prevCmdMenu.addAction(LoadDirectory(self))
        prevCmdMenu = menu.addMenu("Move Channels")
        prevCmdMenu.addAction(SwapChannels(self, self.config, self.osc))
        prevCmdMenu.addAction(CopyChannels(self, self.config, self.osc))
        prevCmdMenu = menu.addMenu("Reset...")
        prevCmdMenu.addAction(ResetCommands(self, self.config, self.widgets, self.osc))
        prevCmdMenu.addAction(ResetCache(self))
        if "iem" in self.config["osc"]:
            menu.addAction(TransferButton(self, self.config, self.osc))
        menu.addAction(UpdateApp(self))

        self.addSubscriptions()
    
    # Load Config Cache
    def loadConfigCache(self):
        if os.path.exists("data/config.cache"):
            with open("data/config.cache") as file:
                self.config = json.load(file)

    # Load Cue Cache
    def loadCueCache(self):
        if os.path.exists("data/cue.cache"):
            with open("data/cue.cache") as file:
                loadCue(file, self.widgets)

    # Save Cache
    def closeEvent(self, a0):
        for window in self.widgets["windows"].copy().keys():
            self.widgets["windows"][window].close()

        for mixerName in self.config["osc"]:
            self.osc[mixerName + "Server"].shutdown()
        self.osc["atemServer"].shutdown()

        if self.saveCache:
            with open("data/config.cache", "w") as file:
                json.dump(self.config, file, indent = 4)

            with open("data/cue.cache", "w") as file:
                saveCue(self.config, file, self.widgets)
        
        self.removeSubscriptions()

        return super().closeEvent(a0)

    def addSubscriptions(self):
        if (
            "selectLink" in self.config
            and "targetDestination" in self.config["selectLink"]
            and "midiChannel" in self.config["selectLink"]
        ):
            self.curSelect = None
            self.osc["fohServer"].subscription.add(SELECT_STAT, self.processSelectSubscription)

        if (
            "talkback" in self.config
            and "link" in self.config["talkback"]
            and "channel" in self.config["talkback"]
            and self.config["talkback"]["link"]
            and "iem" in self.config["osc"]
        ):
            self.tbCurState = -1 # Start at -1, to make sure we start with initializing the state
            self.tbButtonStates = [0, 0]
            for talkbackDestination in ["A", "B"]:
                self.osc["fohServer"].subscription.add(TALKBACK_STAT_PREFIX + talkbackDestination, self.processTalkbackSubscription)

    def removeSubscriptions(self):
        if (
            "selectLink" in self.config
            and "targetDestination" in self.config["selectLink"]
            and "midiChannel" in self.config["selectLink"]
        ):
            self.osc["fohServer"].subscription.remove(SELECT_STAT)

        if (
            "talkback" in self.config
            and "link" in self.config["talkback"]
            and "channel" in self.config["talkback"]
            and self.config["talkback"]["link"]
            and "iem" in self.config["osc"]
        ):
            for talkbackDestination in ["A", "B"]:
                self.osc["fohServer"].subscription.remove(TALKBACK_STAT_PREFIX + talkbackDestination)
            if self.osc["iemClient"].connected:
                self.osc["iemClient"].send_message(self.config["talkback"]["channel"] + "/mix/on", 1)

    def processTalkbackSubscription(self, mixerName, message, arg):
        if message == TALKBACK_STAT_PREFIX + "A":
            self.tbButtonStates[0] = arg

            newState = max(self.tbButtonStates) # If one button is on, then want the talkback gate to be open
            if newState != self.tbCurState:
                self.tbCurState = newState
                self.osc["iemClient"].send_message(self.config["talkback"]["channel"] + "/mix/on", newState)
        else: # B
            self.tbButtonStates[1] = arg
    
    def processSelectSubscription(self, mixerName, message, arg):
        if self.curSelect != arg:
            self.osc[self.config["selectLink"]["targetDestination"] + "Midi"].send(
                mido.Message("note_on", channel = self.config["selectLink"]["midiChannel"] - 1, note = arg)
            )
            self.curSelect = arg

def excepthook(exc_type, exc_value, exc_tb):
    tb = "".join(traceback.format_exception(exc_type, exc_value, exc_tb))
    logging.getLogger("SYSERRR").critical(tb)
    QApplication.quit()
    logFile.close()
    # Copy Log file to tmp directory (Might be too Mac dependent)
    subprocess.Popen("cp ./app.log ~/Library/Logs/" + APP_NAME + "-crash-" + datetime.now().strftime('%Y%m%d%H%M%S') + ".log", shell = True).wait()

os.chdir(os.path.dirname(__file__))
if not os.path.exists("pyinstaller.sh"): # Not in Main Directory
    os.chdir("../Resources")
logFile = open("app.log", "w")
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