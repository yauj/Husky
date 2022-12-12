from PyQt6.QtGui import QColor
from PyQt6.QtWidgets import (
    QComboBox,
    QMessageBox,
    QPushButton,
)
import traceback
from util.constants import BANKS_16, BANKS_32, BANKS_48
from util.customWidgets import ProgressDialog
from util.lock import OwnerLock

# TODO: Create subscription, to change routing if routing changes
class RoutingBox(QComboBox):
    def __init__(self, osc, mixerName, command, options):
        super().__init__()
        self.osc = osc
        self.mixerName = mixerName
        self.command = command
        self.lock = OwnerLock()
        self.setFixedWidth(300)
        self.addItems(options)
        self.setCurrentIndex(-1)
        self.currentIndexChanged.connect(self.changed)
        osc[mixerName + "Server"].subscription.add(command, self.processSubscription)
    
    def changed(self, index):
        try:
            if index >= 0 and self.lock.acquire("button"):
                self.osc[self.mixerName + "Client"].send_message(self.command, index)
        except Exception as ex:
            print(traceback.format_exc())
            dlg = QMessageBox(self)
            dlg.setWindowTitle("Routing")
            dlg.setText("Error: " + str(ex))
            dlg.exec()

    def processSubscription(self, mixerName, message, arg):
        if mixerName == self.mixerName and message == self.command and arg != self.currentIndex():
            if self.lock.acquire(mixerName + " " + message):
                self.setCurrentIndex(arg)

class RoutingSwitchButton(QPushButton):
    def __init__(self, osc, mixerName, tabs):
        super().__init__("Switch Between Record/Play")
        self.osc = osc
        self.mixerName = mixerName
        self.tabs = tabs
        self.pressed.connect(self.clicked)
        self.updateState()

    def clicked(self):
        try:
            newValue = 1 if self.isRecord() else 0
            self.osc[self.mixerName + "Client"].send_message("/config/routing/routswitch", newValue)

            dlg = QMessageBox(self)
            dlg.setWindowTitle("Routing")
            dlg.setText(self.mixerName.upper() + " Routing Swapped")
            dlg.exec()
        except Exception as ex:
            print(traceback.format_exc())
            dlg = QMessageBox(self)
            dlg.setWindowTitle("Routing")
            dlg.setText("Error: " + str(ex))
            dlg.exec()
        
        self.updateState()
        self.setDown(False)
    
    def isRecord(self):
        settings = {"/config/routing/routswitch": None}
        values = self.osc[self.mixerName + "Client"].bulk_send_messages(settings)
        return values["/config/routing/routswitch"] == 0

    def updateState(self):
        try:
            if self.isRecord():
                self.tabs.tabBar().setTabTextColor(0, QColor(0, 255, 0))
                self.tabs.tabBar().setTabTextColor(1, QColor())
            else:
                self.tabs.tabBar().setTabTextColor(0, QColor())
                self.tabs.tabBar().setTabTextColor(1, QColor(0, 255, 0))
        except:
            self.tabs.tabBar().setTabTextColor(0, QColor())
            self.tabs.tabBar().setTabTextColor(1, QColor())

class RoutingPresetButton(QPushButton):
    def __init__(self, name, mixerName, widgets, indexes):
        super().__init__(name + " Routing")
        self.name = name
        self.mixerName = mixerName
        self.widgets = widgets
        self.indexes = indexes
        self.pressed.connect(self.clicked)
    
    def clicked(self):
        try:
            for idx, bank in enumerate(BANKS_32):
                self.widgets["routing"][self.mixerName]["/config/routing/IN/" + bank].setCurrentIndex(self.indexes[idx])
            
            dlg = QMessageBox(self)
            dlg.setWindowTitle("Routing")
            dlg.setText(self.mixerName.upper() + " " + self.name + " Preset Loaded")
            dlg.exec()
        except Exception as ex:
            print(traceback.format_exc())
            dlg = QMessageBox(self)
            dlg.setWindowTitle("Routing")
            dlg.setText("Error: " + str(ex))
            dlg.exec()
        
        self.setDown(False)

class RoutingSyncButton(QPushButton):
    def __init__(self, osc, mixerName, widgets):
        super().__init__("Sync")
        self.osc = osc
        self.mixerName = mixerName
        self.widgets = widgets
        self.pressed.connect(self.clicked)
    
    def clicked(self):
        dlg = ProgressDialog(self.mixerName.upper() + " Routing Sync", self.main)
        dlg.exec()

        self.setDown(False)

    def main(self, dlg):
        try:
            syncRouting(self.osc, self.mixerName, self.widgets)
            dlg.complete.emit()
        except Exception as ex:
            print(traceback.format_exc())
            dlg.raiseException.emit(ex)

def syncRouting(osc, mixerName, widgets, dlg = None):
    values = getCurrentRouting(osc, mixerName, dlg)
    for command in widgets["routing"][mixerName]:
        if values[command] is not None:
            widgets["routing"][mixerName][command].setCurrentIndex(values[command])
        else:
            widgets["routing"][mixerName][command].setCurrentIndex(-1)

def getCurrentRouting(osc, mixerName, dlg = None):
    settings = {}
    for bank in BANKS_32:
        settings["/config/routing/IN/" + bank] = None
        settings["/config/routing/PLAY/" + bank] = None
        settings["/config/routing/CARD/" + bank] = None
    settings["/config/routing/IN/AUX"] = None
    settings["/config/routing/PLAY/AUX"] = None
    for bank in BANKS_48:
        settings["/config/routing/AES50A/" + bank] = None
        settings["/config/routing/AES50B/" + bank] = None
    for bank in BANKS_16:
        settings["/config/routing/OUT/" + bank] = None
    for idx in range(1, 17):
        settings["/outputs/main/" + "{:02d}".format(idx) + "/src"] = None
        settings["/outputs/p16/" + "{:02d}".format(idx) + "/src"] = None
    for idx in range(1, 7):
        settings["/outputs/aux/" + "{:02d}".format(idx) + "/src"] = None
    for idx in range(1, 3):
        settings["/outputs/aes/" + "{:02d}".format(idx) + "/src"] = None
    for idx in range(1, 3):
        settings["/outputs/rec/" + "{:02d}".format(idx) + "/src"] = None
    for idx in range(1, 33):
        settings["/config/userrout/in/" + "{:02d}".format(idx)] = None
    for idx in range(1, 49):
        settings["/config/userrout/out/" + "{:02d}".format(idx)] = None

    if dlg:
        dlg.initBar.emit(len(settings))

    try:
        return osc[mixerName + "Client"].bulk_send_messages(settings, dlg)
    except Exception as ex:
        if dlg:
            raise ex
        else:
            return settings # Return empty values on error