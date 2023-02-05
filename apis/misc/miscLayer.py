from apis.misc.miscGain import GainButton
from apis.misc.miscMutes import MutesButton
from apis.misc.miscReset import ResetButton
from apis.misc.miscRouting import RoutingButton
from apis.misc.miscTalkback import TalkbackButton
from apis.misc.miscTransfer import TransferButton
from PyQt6.QtWidgets import (
    QVBoxLayout,
    QWidget,
)
from util.constants import MIXER_TYPE

class MiscLayer(QWidget):
    def __init__(self, config, widgets, osc):
        super().__init__()

        vlayout = QVBoxLayout()
        if MIXER_TYPE == "X32":
            vlayout.addWidget(TalkbackButton(config, osc))
            if "iem" in config["osc"]:
                vlayout.addWidget(TransferButton(config, osc))
            vlayout.addWidget(RoutingButton(config, widgets, osc))
        vlayout.addWidget(GainButton(config, widgets, osc))
        vlayout.addWidget(MutesButton(config, osc))
        vlayout.addWidget(ResetButton(config, osc))

        self.setLayout(vlayout)