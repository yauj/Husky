from apis.misc.miscReset import ResetButton
from apis.misc.miscRouting import RoutingBox, RoutingSyncButton, getCurrentRouting
from apis.misc.miscTalkback import TalkbackAllButton, TalkbackBox, TalkbackMeButton
from apis.misc.miscTransfer import TransferButton
from PyQt6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QScrollArea,
    QTabWidget,
    QVBoxLayout,
    QWidget,
)
from util.constants import (
    BANKS_16, BANKS_32, BANKS_48,
    ROUTING_IN, ROUTING_IN_AUX, ROUTING_IN_USER,
    ROUTING_OUT, ROUTING_OUT_DIGITAL, ROUTING_OUT_LOCAL_A, ROUTING_OUT_LOCAL_B, ROUTING_OUT_USER
)

class MiscLayer(QTabWidget):
    def __init__(self, config, widgets, osc):
        super().__init__()
        self.config = config
        self.widgets = widgets
        self.osc = osc

        self.addTab(self.talkbackLayer(), "Talkback")
        self.addTab(self.transferLayer(), "FOH->IEM")
        self.addTab(self.routingLayer(), "Routing")
        self.addTab(self.resetLayer(), "Reset")

    def talkbackLayer(self):
        vlayout = QVBoxLayout()

        label = QLabel("Specify who to talkback to. A checked box indicates that talkback is active for channel.")
        label.setMaximumHeight(20)
        vlayout.addWidget(label)
   
        self.talkbacks = {}

        vlayout.addWidget(TalkbackAllButton(self.osc, self.talkbacks))
        for chName in self.config["personal"]:
            if "iem_bus" in self.config["personal"][chName]:
                hlayout = QHBoxLayout()
                hlayout.addWidget(QLabel(chName + ":"))
                hlayout.addWidget(TalkbackMeButton(self.osc, self.talkbacks, chName))
                self.talkbacks[chName] = TalkbackBox(self.config, self.osc, chName)
                spacer = QWidget()
                spacer.setFixedWidth(30)
                hlayout.addWidget(spacer)
                hlayout.addWidget(self.talkbacks[chName])
                vlayout.addLayout(hlayout)

        widget = QWidget()
        widget.setLayout(vlayout)
        return widget
        
    def transferLayer(self):
        vlayout = QVBoxLayout()

        vlayout.addWidget(QLabel("Do you want to transfer Channel EQ, Compression, Mute settings from the FOH Mixer to the IEM Mixer?"))
        vlayout.addWidget(TransferButton(self.config, self.osc))

        widget = QWidget()
        widget.setLayout(vlayout)
        return widget
    
    def routingLayer(self):
        tabs = QTabWidget()
        for mixerName in self.config["osc"]:
            tabs.addTab(self.routingTabLayer(mixerName), mixerName.upper())
        
        return tabs
    
    def routingTabLayer(self, mixerName):
        initValues = getCurrentRouting(self.osc, mixerName)

        vlayout = QVBoxLayout()
        vlayout.addWidget(RoutingSyncButton(self.osc, mixerName, self.widgets))

        tabs = QTabWidget()
        tabs.addTab(self.routingInLayer(mixerName, initValues), "Inputs")
        tabs.addTab(self.routingPatchLayer(mixerName, initValues), "Patches")
        tabs.addTab(self.routingOutputLayer(mixerName, initValues), "Ouputs")
        vlayout.addWidget(tabs)

        widget = QWidget()
        widget.setLayout(vlayout)
        return widget

    def routingInLayer(self, mixerName, initValues):
        vlayout = QVBoxLayout()
        
        for bank in BANKS_32:
            hlayout = QHBoxLayout()
            hlayout.addWidget(QLabel("Channels " + bank + ":"))
            option = RoutingBox(self.osc, mixerName, "/config/routing/IN/" + bank, ROUTING_IN, initValues)
            self.widgets["routing"][mixerName]["/config/routing/IN/" + bank] = option
            hlayout.addWidget(option)
            vlayout.addLayout(hlayout)

        hlayout = QHBoxLayout()
        hlayout.addWidget(QLabel("AUX Channels:"))
        option = RoutingBox(self.osc, mixerName, "/config/routing/IN/AUX", ROUTING_IN_AUX, initValues)
        self.widgets["routing"][mixerName]["/config/routing/IN/AUX"] = option
        hlayout.addWidget(option)
        vlayout.addLayout(hlayout)
        
        widget = QWidget()
        widget.setLayout(vlayout)

        scroll = QScrollArea()
        scroll.setWidget(widget)
        scroll.setWidgetResizable(True)
        return scroll
    
    def routingPatchLayer(self, mixerName, initValues):
        tabs = QTabWidget()

        tabs.addTab(self.routingPatchOutLayer(mixerName, initValues), "Out Patch")
        tabs.addTab(self.routingPatchUserInLayer(mixerName, initValues), "User In")
        tabs.addTab(self.routingPatchUserOutLayer(mixerName, initValues), "User Out")

        return tabs

    def routingPatchOutLayer(self, mixerName, initValues):
        vlayout = QVBoxLayout()
        
        for idx in range(1, 17):
            hlayout = QHBoxLayout()
            hlayout.addWidget(QLabel("Out Patch " + str(idx) + ":"))
            option = RoutingBox(self.osc, mixerName, "/outputs/main/" + "{:02d}".format(idx) + "/src", ROUTING_OUT_DIGITAL, initValues)
            self.widgets["routing"][mixerName]["/outputs/main/" + "{:02d}".format(idx) + "/src"] = option
            hlayout.addWidget(option)
            vlayout.addLayout(hlayout)
        
        widget = QWidget()
        widget.setLayout(vlayout)

        scroll = QScrollArea()
        scroll.setWidget(widget)
        scroll.setWidgetResizable(True)
        return scroll
    
    def routingPatchUserInLayer(self, mixerName, initValues):
        vlayout = QVBoxLayout()
        
        for idx in range(1, 33):
            hlayout = QHBoxLayout()
            hlayout.addWidget(QLabel("User In " + str(idx) + ":"))
            option = RoutingBox(self.osc, mixerName, "/config/userrout/in/" + "{:02d}".format(idx), ROUTING_IN_USER, initValues)
            self.widgets["routing"][mixerName]["/config/userrout/in/" + "{:02d}".format(idx)] = option
            hlayout.addWidget(option)
            vlayout.addLayout(hlayout)
        
        widget = QWidget()
        widget.setLayout(vlayout)

        scroll = QScrollArea()
        scroll.setWidget(widget)
        scroll.setWidgetResizable(True)
        return scroll
    
    def routingPatchUserOutLayer(self, mixerName, initValues):
        vlayout = QVBoxLayout()
        
        for idx in range(1, 49):
            hlayout = QHBoxLayout()
            hlayout.addWidget(QLabel("User Out " + str(idx) + ":"))
            option = RoutingBox(self.osc, mixerName, "/config/userrout/out/" + "{:02d}".format(idx), ROUTING_OUT_USER, initValues)
            self.widgets["routing"][mixerName]["/config/userrout/out/" + "{:02d}".format(idx)] = option
            hlayout.addWidget(option)
            vlayout.addLayout(hlayout)
        
        widget = QWidget()
        widget.setLayout(vlayout)

        scroll = QScrollArea()
        scroll.setWidget(widget)
        scroll.setWidgetResizable(True)
        return scroll

    def routingOutputLayer(self, mixerName, initValues):
        tabs = QTabWidget()

        tabs.addTab(self.routingOutputAESLayer(mixerName, initValues, "A"), "AES-A")
        tabs.addTab(self.routingOutputAESLayer(mixerName, initValues, "B"), "AES-B")
        tabs.addTab(self.routingOutputCardLayer(mixerName, initValues), "Card")
        tabs.addTab(self.routingOutputLocalLayer(mixerName, initValues), "Local")
        tabs.addTab(self.routingOutputP16Layer(mixerName, initValues), "P16")
        tabs.addTab(self.routingOutputOtherLayer(mixerName, initValues), "Other")

        return tabs

    def routingOutputAESLayer(self, mixerName, initValues, portName):
        vlayout = QVBoxLayout()
        
        for bank in BANKS_48:
            hlayout = QHBoxLayout()
            hlayout.addWidget(QLabel("AES-" + portName + " Output " + bank + ":"))
            option = RoutingBox(self.osc, mixerName, "/config/routing/AES50" + portName + "/" + bank, ROUTING_OUT, initValues)
            self.widgets["routing"][mixerName]["/config/routing/AES50" + portName + "/" + bank] = option
            hlayout.addWidget(option)
            vlayout.addLayout(hlayout)
        
        widget = QWidget()
        widget.setLayout(vlayout)

        scroll = QScrollArea()
        scroll.setWidget(widget)
        scroll.setWidgetResizable(True)
        return scroll
    
    def routingOutputCardLayer(self, mixerName, initValues):
        vlayout = QVBoxLayout()
        
        for bank in BANKS_32:
            hlayout = QHBoxLayout()
            hlayout.addWidget(QLabel("Card Output " + bank + ":"))
            option = RoutingBox(self.osc, mixerName, "/config/routing/CARD/" + bank, ROUTING_OUT, initValues)
            self.widgets["routing"][mixerName]["/config/routing/CARD/" + bank] = option
            hlayout.addWidget(option)
            vlayout.addLayout(hlayout)
        
        widget = QWidget()
        widget.setLayout(vlayout)

        scroll = QScrollArea()
        scroll.setWidget(widget)
        scroll.setWidgetResizable(True)
        return scroll
    
    def routingOutputLocalLayer(self, mixerName, initValues):
        vlayout = QVBoxLayout()
        
        for idx, bank in enumerate(BANKS_16):
            hlayout = QHBoxLayout()
            hlayout.addWidget(QLabel("Local XLR Output " + bank + ":"))
            lst = ROUTING_OUT_LOCAL_A if idx % 2 == 0 else ROUTING_OUT_LOCAL_B
            option = RoutingBox(self.osc, mixerName, "/config/routing/OUT/" + bank, lst, initValues)
            self.widgets["routing"][mixerName]["/config/routing/OUT/" + bank] = option
            hlayout.addWidget(option)
            vlayout.addLayout(hlayout)
        
        for idx in range(1, 7):
            hlayout = QHBoxLayout()
            hlayout.addWidget(QLabel("Local AUX Output " + str(idx) + ":"))
            option = RoutingBox(self.osc, mixerName, "/outputs/aux/" + "{:02d}".format(idx) + "/src", ROUTING_OUT_DIGITAL, initValues)
            self.widgets["routing"][mixerName]["/outputs/aux/" + "{:02d}".format(idx) + "/src"] = option
            hlayout.addWidget(option)
            vlayout.addLayout(hlayout)
        
        widget = QWidget()
        widget.setLayout(vlayout)

        scroll = QScrollArea()
        scroll.setWidget(widget)
        scroll.setWidgetResizable(True)
        return scroll

    def routingOutputP16Layer(self, mixerName, initValues):
        vlayout = QVBoxLayout()
        
        for idx in range(1, 17):
            hlayout = QHBoxLayout()
            hlayout.addWidget(QLabel("P16 " + str(idx) + ":"))
            option = RoutingBox(self.osc, mixerName, "/outputs/p16/" + "{:02d}".format(idx) + "/src", ROUTING_OUT_DIGITAL, initValues)
            self.widgets["routing"][mixerName]["/outputs/p16/" + "{:02d}".format(idx) + "/src"] = option
            hlayout.addWidget(option)
            vlayout.addLayout(hlayout)
        
        widget = QWidget()
        widget.setLayout(vlayout)

        scroll = QScrollArea()
        scroll.setWidget(widget)
        scroll.setWidgetResizable(True)
        return scroll

    def routingOutputOtherLayer(self, mixerName, initValues):
        vlayout = QVBoxLayout()
        
        for idx, label in enumerate(["L", "R"]):
            hlayout = QHBoxLayout()
            hlayout.addWidget(QLabel("AES " + label + ":"))
            option = RoutingBox(self.osc, mixerName, "/outputs/aes/" + "{:02d}".format(idx + 1) + "/src", ROUTING_OUT_DIGITAL, initValues)
            self.widgets["routing"][mixerName]["/outputs/aes/" + "{:02d}".format(idx + 1) + "/src"] = option
            hlayout.addWidget(option)
            vlayout.addLayout(hlayout)

        for idx, label in enumerate(["L", "R"]):
            hlayout = QHBoxLayout()
            hlayout.addWidget(QLabel("USB Recording " + label + ":"))
            option = RoutingBox(self.osc, mixerName, "/outputs/rec/" + "{:02d}".format(idx + 1) + "/src", ROUTING_OUT_DIGITAL, initValues)
            self.widgets["routing"][mixerName]["/outputs/rec/" + "{:02d}".format(idx + 1) + "/src"] = option
            hlayout.addWidget(option)
            vlayout.addLayout(hlayout)
        
        widget = QWidget()
        widget.setLayout(vlayout)

        scroll = QScrollArea()
        scroll.setWidget(widget)
        scroll.setWidgetResizable(True)
        return scroll

    def resetLayer(self):
        vlayout = QVBoxLayout()

        vlayout.addWidget(QLabel("Do you want to reset Mute, Pan and Fader settings of the FOH mixer?"))
        vlayout.addWidget(ResetButton(self.config, self.osc))

        widget = QWidget()
        widget.setLayout(vlayout)
        return widget