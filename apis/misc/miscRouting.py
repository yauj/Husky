from PyQt6.QtWidgets import (
    QComboBox,
    QMessageBox,
    QPushButton,
)
import traceback
from util.constants import BANKS_16, BANKS_32, BANKS_48
from util.customWidgets import ProgressDialog

class RoutingBox(QComboBox):
    def __init__(self, osc, mixerName, command, options, initValues):
        super().__init__()
        self.osc = osc
        self.mixerName = mixerName
        self.command = command
        self.setFixedWidth(300)
        self.addItems(options)
        if initValues[command] is None:
            self.setCurrentIndex(-1)
        else:
            self.setCurrentIndex(initValues[command])
        self.currentIndexChanged.connect(self.changed)
    
    def changed(self, index):
        try:
            if index >= 0:
                self.osc[self.mixerName + "Client"].send_message(self.command, index)
        except Exception as ex:
            print(traceback.format_exc())
            dlg = QMessageBox(self)
            dlg.setWindowTitle("Routing")
            dlg.setText("Error: " + str(ex))
            dlg.exec()

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
        settings["/config/routing/CARD/" + bank] = None
    settings["/config/routing/IN/AUX"] = None
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