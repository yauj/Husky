import logging
from PyQt6.QtWidgets import (
    QCheckBox,
    QDialog,
    QGridLayout,
    QLabel,
    QMessageBox,
    QPushButton,
    QScrollArea,
    QTabWidget,
    QVBoxLayout,
    QWidget,
)
import traceback
from util.constants import (ALL_CHANNELS)

logger = logging.getLogger(__name__)

class MutesButton(QPushButton):
    def __init__(self, config, osc):
        super().__init__("Mute Settings")
        self.config = config
        self.osc = osc
        self.pressed.connect(self.clicked)
    
    def clicked(self):
        MutesDialog(self.config, self.osc).exec()
        self.setDown(False)

class MutesDialog(QDialog):
    def __init__(self, config, osc):
        super().__init__()
        self.config = config
        self.osc = osc

        vlayout = QVBoxLayout()

        vlayout.addWidget(QLabel("Checkbox will be checked if it's muted."))

        if len(self.config["osc"]) == 1:
            for mixerName in self.config["osc"]:
                vlayout.addWidget(self.mutesLayer(mixerName)) 
        else:
            tabs = QTabWidget()
            for mixerName in self.config["osc"]:
                tabs.addTab(self.mutesLayer(mixerName), mixerName.upper())
            vlayout.addWidget(tabs)

        self.setLayout(vlayout)

    def mutesLayer(self, mixerName):
        try:
            initValues = getCurrentMutes(self.osc, mixerName)
            layout = QGridLayout()

            for idx, channel in enumerate(ALL_CHANNELS):
                label = channel
                if "/ch/" in channel:
                    label = "Ch " + "".join(channel.split("/ch/")) 
                elif "/auxin/" in channel:
                    label = "AUX " + "".join(channel.split("/auxin/"))
                elif "/fxrtn/" in channel:
                    label = "FX " + "".join(channel.split("/fxrtn/"))

                layout.addWidget(QLabel(label), (idx // 8) * 2, idx % 8)
                layout.addWidget(MutesBox(self.osc, mixerName, channel + "/mix/on", initValues), ((idx // 8) * 2) + 1, idx % 8)
            
            widget = QWidget()
            widget.setLayout(layout)

            scroll = QScrollArea()
            scroll.setWidget(widget)
            scroll.setWidgetResizable(True)
            return scroll
        except Exception as ex:
            logger.error(traceback.format_exc())
            vlayout = QVBoxLayout()
            label = QLabel("Error: " + str(ex))
            label.setStyleSheet("color:red")
            vlayout.addWidget(label)
            
            widget = QWidget()
            widget.setLayout(vlayout)
            return widget

class MutesBox(QCheckBox):
    def __init__(self, osc, mixerName, command, initValues):
        super().__init__()
        self.osc = osc
        self.mixerName = mixerName
        self.command = command
        self.setStyleSheet("\
            QCheckBox::indicator { border: 1px solid; border-color: gray; }\
            QCheckBox::indicator:checked { background-color: red; }\
        ")
        self.setChecked(initValues[command] == 0 if initValues[command] is not None else False)
        self.stateChanged.connect(self.changed)
    
    def changed(self, state):
        try:
            self.osc[self.mixerName + "Client"].send_message(self.command, 0 if state > 0 else 1)
        except Exception as ex:
            logger.error(traceback.format_exc())
            dlg = QMessageBox(self)
            dlg.setWindowTitle("Routing")
            dlg.setText("Error: " + str(ex))
            dlg.exec()

def getCurrentMutes(osc, mixerName, dlg = None):
    settings = {}
    for channel in ALL_CHANNELS:
        settings[channel + "/mix/on"] = None

    if dlg:
        dlg.initBar.emit(len(settings))

    return osc[mixerName + "Client"].bulk_send_messages(settings, dlg)