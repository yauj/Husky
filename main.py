from apis.connection.connectionLayer import ConnectionLayer
from apis.cues.cueLayer import CueLayer
from apis.cues.cueLoad import loadCue
from apis.cues.cueSave import saveCue
from apis.menu.About import About
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
from util.constants import APP_NAME
from util.defaultOSC import MIDIVirtualPort

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.config = config
        self.widgets = {"connection": {}, "personal": {}, "tabs": {}, "cues": [], "faders": [], "routing": {}, "windows": {}}
        self.osc = {}
        self.saveCache = True
        self.virtualPort = MIDIVirtualPort() # Virtual MIDI Port

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
        prevCmdMenu = menu.addMenu("Reset...")
        prevCmdMenu.addAction(ResetCommands(self, self.config, self.widgets, self.osc))
        prevCmdMenu.addAction(ResetCache(self))
        menu.addAction(SwapChannels(self, self.config, self.osc))
        if "iem" in self.config["osc"]:
            menu.addAction(TransferButton(self, self.config, self.osc))
        menu.addAction(UpdateApp(self))
    
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

        return super().closeEvent(a0)

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