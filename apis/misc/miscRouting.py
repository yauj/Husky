from PyQt6.QtGui import QColor
from PyQt6.QtWidgets import (
    QComboBox,
    QDialog,
    QHBoxLayout,
    QLabel,
    QMessageBox,
    QPushButton,
    QScrollArea,
    QTabWidget,
    QVBoxLayout,
    QWidget,
)
import traceback
from util.constants import (
    BANKS_16, BANKS_32, BANKS_48,
    ROUTING_IN, ROUTING_IN_AUX, ROUTING_IN_USER,
    ROUTING_OUT, ROUTING_OUT_DIGITAL, ROUTING_OUT_LOCAL_A, ROUTING_OUT_LOCAL_B, ROUTING_OUT_USER
)
from util.customWidgets import ProgressDialog

class RoutingButton(QPushButton):
    def __init__(self, config, widgets, osc):
        super().__init__("Modify Routing Settings")
        self.config = config
        self.widgets = widgets
        self.osc = osc
        self.pressed.connect(self.clicked)
    
    def clicked(self):
        RoutingDialog(self.config, self.widgets, self.osc).exec()
        self.setDown(False)

class RoutingDialog(QDialog):
    def __init__(self, config, widgets, osc):
        super().__init__()
        self.config = config
        self.widgets = widgets
        self.osc = osc

        vlayout = QVBoxLayout()

        tabs = QTabWidget()
        for mixerName in self.config["osc"]:
            tabs.addTab(self.routingTabLayer(mixerName), mixerName.upper())
        
        vlayout.addWidget(tabs)
        self.setLayout(vlayout)

    def routingTabLayer(self, mixerName):
        vlayout = QVBoxLayout()
        vlayout.addWidget(RoutingSyncButton(self.osc, mixerName, self.widgets))

        tabs = QTabWidget()
        tabs.addTab(self.routingInLayer(mixerName), "Inputs")
        tabs.addTab(self.routingPatchLayer(mixerName), "Patches")
        tabs.addTab(self.routingOutputLayer(mixerName), "Ouputs")
        vlayout.addWidget(tabs)

        widget = QWidget()
        widget.setLayout(vlayout)
        return widget

    def routingInLayer(self, mixerName):
        vlayout = QVBoxLayout()

        tabs = QTabWidget()
        tabs.addTab(self.routingInTabLayer(mixerName, "IN"), "Record")
        tabs.addTab(self.routingInTabLayer(mixerName, "PLAY"), "Play")

        self.widgets["routingSwap"][mixerName] = RoutingSwitchButton(self.osc, mixerName, tabs)

        vlayout.addWidget(self.widgets["routingSwap"][mixerName])
        vlayout.addWidget(tabs)
        
        widget = QWidget()
        widget.setLayout(vlayout)
        return widget

    def routingInTabLayer(self, mixerName, mapping):
        vlayout = QVBoxLayout()

        hlayout = QHBoxLayout()
        hlayout.addWidget(RoutingPresetButton("AES-A", mixerName, self.widgets, range(4, 8)))
        hlayout.addWidget(RoutingPresetButton("AES-B", mixerName, self.widgets, range(10, 14)))
        hlayout.addWidget(RoutingPresetButton("Card", mixerName, self.widgets, range(16, 20)))
        hlayout.addWidget(RoutingPresetButton("User In", mixerName, self.widgets, range(20, 24)))
        vlayout.addLayout(hlayout)
        
        for bank in BANKS_32:
            hlayout = QHBoxLayout()
            hlayout.addWidget(QLabel("Channels " + bank + ":"))
            option = RoutingBox(self.osc, mixerName, "/config/routing/" + mapping + "/" + bank, ROUTING_IN)
            self.widgets["routing"][mixerName]["/config/routing/" + mapping + "/" + bank] = option
            hlayout.addWidget(option)
            vlayout.addLayout(hlayout)

        hlayout = QHBoxLayout()
        hlayout.addWidget(QLabel("AUX Channels:"))
        option = RoutingBox(self.osc, mixerName, "/config/routing/" + mapping + "/AUX", ROUTING_IN_AUX)
        self.widgets["routing"][mixerName]["/config/routing/" + mapping + "/AUX"] = option
        hlayout.addWidget(option)
        vlayout.addLayout(hlayout)
        
        widget = QWidget()
        widget.setLayout(vlayout)

        scroll = QScrollArea()
        scroll.setWidget(widget)
        scroll.setWidgetResizable(True)
        return scroll
    
    def routingPatchLayer(self, mixerName):
        tabs = QTabWidget()

        tabs.addTab(self.routingPatchOutLayer(mixerName), "Out Patch")
        tabs.addTab(self.routingPatchUserInLayer(mixerName), "User In")
        tabs.addTab(self.routingPatchUserOutLayer(mixerName), "User Out")

        return tabs

    def routingPatchOutLayer(self, mixerName):
        vlayout = QVBoxLayout()
        
        for idx in range(1, 17):
            hlayout = QHBoxLayout()
            hlayout.addWidget(QLabel("Out Patch " + str(idx) + ":"))
            option = RoutingBox(self.osc, mixerName, "/outputs/main/" + "{:02d}".format(idx) + "/src", ROUTING_OUT_DIGITAL)
            self.widgets["routing"][mixerName]["/outputs/main/" + "{:02d}".format(idx) + "/src"] = option
            hlayout.addWidget(option)
            vlayout.addLayout(hlayout)
        
        widget = QWidget()
        widget.setLayout(vlayout)

        scroll = QScrollArea()
        scroll.setWidget(widget)
        scroll.setWidgetResizable(True)
        return scroll
    
    def routingPatchUserInLayer(self, mixerName):
        vlayout = QVBoxLayout()
        
        for idx in range(1, 33):
            hlayout = QHBoxLayout()
            hlayout.addWidget(QLabel("User In " + str(idx) + ":"))
            option = RoutingBox(self.osc, mixerName, "/config/userrout/in/" + "{:02d}".format(idx), ROUTING_IN_USER)
            self.widgets["routing"][mixerName]["/config/userrout/in/" + "{:02d}".format(idx)] = option
            hlayout.addWidget(option)
            vlayout.addLayout(hlayout)
        
        widget = QWidget()
        widget.setLayout(vlayout)

        scroll = QScrollArea()
        scroll.setWidget(widget)
        scroll.setWidgetResizable(True)
        return scroll
    
    def routingPatchUserOutLayer(self, mixerName):
        vlayout = QVBoxLayout()
        
        for idx in range(1, 49):
            hlayout = QHBoxLayout()
            hlayout.addWidget(QLabel("User Out " + str(idx) + ":"))
            option = RoutingBox(self.osc, mixerName, "/config/userrout/out/" + "{:02d}".format(idx), ROUTING_OUT_USER)
            self.widgets["routing"][mixerName]["/config/userrout/out/" + "{:02d}".format(idx)] = option
            hlayout.addWidget(option)
            vlayout.addLayout(hlayout)
        
        widget = QWidget()
        widget.setLayout(vlayout)

        scroll = QScrollArea()
        scroll.setWidget(widget)
        scroll.setWidgetResizable(True)
        return scroll

    def routingOutputLayer(self, mixerName):
        tabs = QTabWidget()

        tabs.addTab(self.routingOutputAESLayer(mixerName, "A"), "AES-A")
        tabs.addTab(self.routingOutputAESLayer(mixerName, "B"), "AES-B")
        tabs.addTab(self.routingOutputCardLayer(mixerName), "Card")
        tabs.addTab(self.routingOutputLocalLayer(mixerName), "Local")
        tabs.addTab(self.routingOutputP16Layer(mixerName), "P16")
        tabs.addTab(self.routingOutputOtherLayer(mixerName), "Other")

        return tabs

    def routingOutputAESLayer(self, mixerName, portName):
        vlayout = QVBoxLayout()
        
        for bank in BANKS_48:
            hlayout = QHBoxLayout()
            hlayout.addWidget(QLabel("AES-" + portName + " Output " + bank + ":"))
            option = RoutingBox(self.osc, mixerName, "/config/routing/AES50" + portName + "/" + bank, ROUTING_OUT)
            self.widgets["routing"][mixerName]["/config/routing/AES50" + portName + "/" + bank] = option
            hlayout.addWidget(option)
            vlayout.addLayout(hlayout)
        
        widget = QWidget()
        widget.setLayout(vlayout)

        scroll = QScrollArea()
        scroll.setWidget(widget)
        scroll.setWidgetResizable(True)
        return scroll
    
    def routingOutputCardLayer(self, mixerName):
        vlayout = QVBoxLayout()
        
        for bank in BANKS_32:
            hlayout = QHBoxLayout()
            hlayout.addWidget(QLabel("Card Output " + bank + ":"))
            option = RoutingBox(self.osc, mixerName, "/config/routing/CARD/" + bank, ROUTING_OUT)
            self.widgets["routing"][mixerName]["/config/routing/CARD/" + bank] = option
            hlayout.addWidget(option)
            vlayout.addLayout(hlayout)
        
        widget = QWidget()
        widget.setLayout(vlayout)

        scroll = QScrollArea()
        scroll.setWidget(widget)
        scroll.setWidgetResizable(True)
        return scroll
    
    def routingOutputLocalLayer(self, mixerName):
        vlayout = QVBoxLayout()
        
        for idx, bank in enumerate(BANKS_16):
            hlayout = QHBoxLayout()
            hlayout.addWidget(QLabel("Local XLR Output " + bank + ":"))
            lst = ROUTING_OUT_LOCAL_A if idx % 2 == 0 else ROUTING_OUT_LOCAL_B
            option = RoutingBox(self.osc, mixerName, "/config/routing/OUT/" + bank, lst)
            self.widgets["routing"][mixerName]["/config/routing/OUT/" + bank] = option
            hlayout.addWidget(option)
            vlayout.addLayout(hlayout)
        
        for idx in range(1, 7):
            hlayout = QHBoxLayout()
            hlayout.addWidget(QLabel("Local AUX Output " + str(idx) + ":"))
            option = RoutingBox(self.osc, mixerName, "/outputs/aux/" + "{:02d}".format(idx) + "/src", ROUTING_OUT_DIGITAL)
            self.widgets["routing"][mixerName]["/outputs/aux/" + "{:02d}".format(idx) + "/src"] = option
            hlayout.addWidget(option)
            vlayout.addLayout(hlayout)
        
        widget = QWidget()
        widget.setLayout(vlayout)

        scroll = QScrollArea()
        scroll.setWidget(widget)
        scroll.setWidgetResizable(True)
        return scroll

    def routingOutputP16Layer(self, mixerName):
        vlayout = QVBoxLayout()
        
        for idx in range(1, 17):
            hlayout = QHBoxLayout()
            hlayout.addWidget(QLabel("P16 " + str(idx) + ":"))
            option = RoutingBox(self.osc, mixerName, "/outputs/p16/" + "{:02d}".format(idx) + "/src", ROUTING_OUT_DIGITAL)
            self.widgets["routing"][mixerName]["/outputs/p16/" + "{:02d}".format(idx) + "/src"] = option
            hlayout.addWidget(option)
            vlayout.addLayout(hlayout)
        
        widget = QWidget()
        widget.setLayout(vlayout)

        scroll = QScrollArea()
        scroll.setWidget(widget)
        scroll.setWidgetResizable(True)
        return scroll

    def routingOutputOtherLayer(self, mixerName):
        vlayout = QVBoxLayout()
        
        for idx, label in enumerate(["L", "R"]):
            hlayout = QHBoxLayout()
            hlayout.addWidget(QLabel("AES " + label + ":"))
            option = RoutingBox(self.osc, mixerName, "/outputs/aes/" + "{:02d}".format(idx + 1) + "/src", ROUTING_OUT_DIGITAL)
            self.widgets["routing"][mixerName]["/outputs/aes/" + "{:02d}".format(idx + 1) + "/src"] = option
            hlayout.addWidget(option)
            vlayout.addLayout(hlayout)

        for idx, label in enumerate(["L", "R"]):
            hlayout = QHBoxLayout()
            hlayout.addWidget(QLabel("USB Recording " + label + ":"))
            option = RoutingBox(self.osc, mixerName, "/outputs/rec/" + "{:02d}".format(idx + 1) + "/src", ROUTING_OUT_DIGITAL)
            self.widgets["routing"][mixerName]["/outputs/rec/" + "{:02d}".format(idx + 1) + "/src"] = option
            hlayout.addWidget(option)
            vlayout.addLayout(hlayout)
        
        widget = QWidget()
        widget.setLayout(vlayout)

        scroll = QScrollArea()
        scroll.setWidget(widget)
        scroll.setWidgetResizable(True)
        return scroll


class RoutingBox(QComboBox):
    def __init__(self, osc, mixerName, command, options):
        super().__init__()
        self.osc = osc
        self.mixerName = mixerName
        self.command = command
        self.setFixedWidth(300)
        self.addItems(options)
        self.setCurrentIndex(-1)
        self.activated.connect(self.changed)
        osc[mixerName + "Server"].subscription.add(command, self.processSubscription)
    
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

    def processSubscription(self, mixerName, message, arg):
        if mixerName == self.mixerName and message == self.command and arg != self.currentIndex():
            self.setCurrentIndex(arg)

class RoutingSwitchButton(QPushButton):
    def __init__(self, osc, mixerName, tabs):
        super().__init__("Switch Between Record/Play")
        self.osc = osc
        self.mixerName = mixerName
        self.tabs = tabs
        self.isRecord = True
        self.pressed.connect(self.onPressed)
        osc[mixerName + "Server"].subscription.add("/config/routing/routswitch", self.processSubscription)

    def onPressed(self):
        try:
            newValue = 1 if self.isRecord else 0
            self.osc[self.mixerName + "Client"].send_message("/config/routing/routswitch", newValue)
            self.isRecord = not self.isRecord

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
    
    def processSubscription(self, mixerName, message, arg):
        self.isRecord = arg == 0
        self.updateState()

    def updateState(self):
        try:
            if self.isRecord:
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