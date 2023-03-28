import logging
from PyQt6.QtCore import (
    Qt
)
from PyQt6.QtGui import (
    QAction,
)
from PyQt6.QtWidgets import (
    QComboBox,
    QDialog,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QVBoxLayout,
)
import traceback
from util.constants import ADDITIONAL_SETTINGS, ALL_CHANNELS, AUX_CHANNELS, SETTINGS
from util.customWidgets import ProgressDialog

logger = logging.getLogger(__name__)

class CopyChannels(QAction):
    def __init__(self, parent, config, osc):
        super().__init__("Copy Channels", parent)
        self.parent = parent
        self.triggered.connect(CopyChannelsDialog(parent, config, osc).exec)

class CopyChannelsDialog(QDialog):
    def __init__(self, parent, config, osc):
        super().__init__(parent)
        self.parent = parent
        self.copyButton = CopyButton(parent, config, osc)

        vlayout = QVBoxLayout()
        vlayout.addWidget(QLabel(
            "Copy all configurations associated to one channel to another channel.\n" +
            "Would recommend using Swap Channels over this, because this is destructive.\n" +
            "Note that this doesn't work well with linked channels.\n" +
            "You should unlink channels before running this."
        ))
        hlayout = QHBoxLayout()
        hlayout.addWidget(self.copyButton.channel1)
        label = QLabel("->")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        hlayout.addWidget(label)
        hlayout.addWidget(self.copyButton.channel2)
        vlayout.addLayout(hlayout)
        vlayout.addWidget(self.copyButton)
        self.setLayout(vlayout)

class CopyButton(QPushButton):
    def __init__(self, parent, config, osc):
        super().__init__("Copy", parent)
        self.parent = parent
        self.config = config
        self.osc = osc

        channels = sorted(set(ALL_CHANNELS) - set(AUX_CHANNELS))
        self.channel1 = QComboBox(parent)
        self.channel1.addItems(channels)
        self.channel1.setFixedWidth(100)
        self.channel2 = QComboBox(parent)
        self.channel2.addItems(channels)
        self.channel2.setFixedWidth(100)

        self.pressed.connect(self.onPressed)
    
    def onPressed(self):
        newDlg = ProgressDialog("Channels Copy", self.main)
        newDlg.exec()
    
    def main(self, dlg):
        try:
            if self.channel1.currentText() != self.channel2.currentText():
                # Init Settings Map
                settings = {}
                for mixerName in self.config["osc"]:
                    if self.osc[mixerName + "Client"].connected:
                        settings[mixerName] = {}

                        # Transfer Gain, if Possible
                        command1 = "/-ha/" + "{:02d}".format(self.channel1.currentIndex()) + "/index"
                        command2 = "/-ha/" + "{:02d}".format(self.channel2.currentIndex()) + "/index"
                        values = self.osc[mixerName + "Client"].bulk_send_messages({command1: None, command2: None})
                        ch1ha = values[command1]
                        ch2ha = values[command2]

                        if ch1ha > -1 and ch2ha > -1:
                            command1 = "/headamp/" + "{:03d}".format(int(ch1ha)) + "/gain"
                            command2 = "/headamp/" + "{:03d}".format(int(ch2ha)) + "/gain"
                            values = self.osc[mixerName + "Client"].bulk_send_messages({command1: None})
                            self.osc[mixerName + "Client"].bulk_send_messages({command2: values[command1]})

                # Fill Settings Map
                for mixerName in settings:
                    for category in SETTINGS:
                        for param in SETTINGS[category]:
                            settings[mixerName][self.channel1.currentText() + param] = None
                    for category in ADDITIONAL_SETTINGS:
                        for param in ADDITIONAL_SETTINGS[category]:
                            settings[mixerName][self.channel1.currentText() + param] = None
                
                # Init Dlg Length
                length = 0
                for mixerName in settings:
                    length += len(settings[mixerName])
                dlg.initBar.emit(length * 2)

                # Fire Commands
                for mixerName in settings:
                    values = self.osc[mixerName + "Client"].bulk_send_messages(settings[mixerName], dlg)
                    newValues = {}
                    for command in values:
                        newCommand = command.replace(self.channel1.currentText(), self.channel2.currentText())
                        newValues[newCommand] = values[command]
                    self.osc[mixerName + "Client"].bulk_send_messages(newValues, dlg)
                
                logger.info("Channels Copyied")
            dlg.complete.emit()
        except Exception as ex:
            logger.error(traceback.format_exc())
            dlg.raiseException.emit(ex)