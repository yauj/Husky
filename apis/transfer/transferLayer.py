import sys
sys.path.insert(0, '../')

from apis.transfer.transferSettings import TransferButton
from PyQt6.QtWidgets import (
    QLabel,
    QVBoxLayout,
    QWidget,
)

class TransferLayer(QWidget):
    def __init__(self, osc):
        super().__init__()
        self.osc = osc
        
        vlayout = QVBoxLayout()

        vlayout.addWidget(QLabel("Do you want to transfer Channel EQ, Compression, Mute settings from the FOH Mixer to the IEM Mixer?"))
        vlayout.addWidget(TransferButton(self.osc))

        widget = QWidget()
        widget.setLayout(vlayout)

        self.setLayout(vlayout)