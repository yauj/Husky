import logging
from PyQt6.QtGui import (
    QAction,
)
from PyQt6.QtWidgets import (
    QMessageBox,
)
import traceback
from util.constants import ALL_CHANNELS, AUX_CHANNELS, LINK_CHANNELS, SETTINGS
from util.customWidgets import ProgressDialog

logger = logging.getLogger(__name__)

class TransferButton(QAction):
    def __init__(self, s, config, osc):
        super().__init__("&Transfer Settings from FOH to IEM Mixer", s)
        self.s = s
        self.config = config
        self.osc = osc
        self.triggered.connect(self.clicked)
    
    def clicked(self):
        dlg = QMessageBox(self.s)
        dlg.setWindowTitle("Transfer")
        dlg.setText(
            "Are you sure you want to transfer settings?\n" + 
            "This will transfer channel config, EQ, dynamics, mute and pan settings from the FOH mixer to the IEM mixer."
        )
        dlg.setStandardButtons(QMessageBox.StandardButton.Ok | QMessageBox.StandardButton.Cancel)
        if dlg.exec() == QMessageBox.StandardButton.Ok:
            newDlg = ProgressDialog("Settings Transfer", self.main)
            newDlg.exec()

    def main(self, dlg):
        try:
            settings = {}

            # Copy Channel Links
            tbNum = self.config["talkback"]["channel"].replace("/ch/", "")
            for chlink in LINK_CHANNELS:
                if tbNum not in chlink:
                    settings["/config/chlink/" + chlink] = None

            # Exclude AUX and talkback channels
            channels = set(ALL_CHANNELS) - set(AUX_CHANNELS)
            if "talkback" in self.config and "channel" in self.config["talkback"]:
                channels = channels - set([self.config["talkback"]["channel"]])
            for channel in channels:
                for category in SETTINGS:
                    for param in SETTINGS[category]:
                        settings[channel + param] = None

            dlg.initBar.emit(len(settings) * 2)
            
            values = self.osc["fohClient"].bulk_send_messages(settings, dlg)
            self.osc["iemClient"].bulk_send_messages(values, dlg)
            
            logger.info("Settings Transferred")
            dlg.complete.emit()
        except Exception as ex:
            logger.error(traceback.format_exc())
            dlg.raiseException.emit(ex)