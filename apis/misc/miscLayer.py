from apis.misc.miscReset import ResetButton
from apis.misc.miscRouting import RoutingButton
from apis.misc.miscTalkback import TalkbackButton
from apis.misc.miscTransfer import TransferButton
from PyQt6.QtWidgets import (
    QVBoxLayout,
    QWidget,
)

class MiscLayer(QWidget):
    def __init__(self, config, widgets, osc):
        super().__init__()
        self.config = config
        self.widgets = widgets
        self.osc = osc

        vlayout = QVBoxLayout()
        vlayout.addWidget(TalkbackButton(self.config, self.osc))
        vlayout.addWidget(RoutingButton(self.config, self.widgets, self.osc))
        vlayout.addWidget(TransferButton(self.config, self.osc))
        vlayout.addWidget(ResetButton(self.config, self.osc))

        self.setLayout(vlayout)