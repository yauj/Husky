import sys
from apis.misc.miscReset import ResetButton
sys.path.insert(0, '../')

from apis.misc.miscTransfer import TransferButton
from PyQt6.QtWidgets import (
    QLabel,
    QTabWidget,
    QVBoxLayout,
    QWidget,
)

class MiscLayer(QTabWidget):
    def __init__(self, config, osc):
        super().__init__()
        self.config = config
        self.osc = osc

        self.addTab(self.transferLayer(), "FOH->IEM")
        self.addTab(self.resetLayer(), "Reset")
        
    def transferLayer(self):
        vlayout = QVBoxLayout()

        vlayout.addWidget(QLabel("Do you want to transfer Channel EQ, Compression, Mute settings from the FOH Mixer to the IEM Mixer?"))
        vlayout.addWidget(TransferButton(self.osc))

        widget = QWidget()
        widget.setLayout(vlayout)
        return widget

    def resetLayer(self):
        vlayout = QVBoxLayout()

        vlayout.addWidget(QLabel("Do you want to reset Mute, Pan and Fader settings of the FOH mixer?"))
        vlayout.addWidget(ResetButton(self.config, self.osc))

        widget = QWidget()
        widget.setLayout(vlayout)
        return widget