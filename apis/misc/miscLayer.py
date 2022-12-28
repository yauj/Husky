from apis.misc.miscGain import GainButton
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

        vlayout = QVBoxLayout()
        if osc["fohClient"].mixerType == "X32":
            vlayout.addWidget(TalkbackButton(config, osc))
            if "iem" in config["osc"]:
                vlayout.addWidget(TransferButton(config, osc))
            vlayout.addWidget(RoutingButton(config, widgets, osc))
        vlayout.addWidget(GainButton(config, widgets, osc))
        vlayout.addWidget(ResetButton(config, osc))

        self.setLayout(vlayout)