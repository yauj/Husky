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

        widgets["misc"]["talkback"] = TalkbackButton(config, osc)
        widgets["misc"]["transfer"] = TransferButton(config, osc)
        widgets["misc"]["routing"] = RoutingButton(config, widgets, osc)

        vlayout.addWidget(widgets["misc"]["talkback"])
        if "iem" in config["osc"]:
            vlayout.addWidget(widgets["misc"]["transfer"])
        vlayout.addWidget(widgets["misc"]["routing"])
        vlayout.addWidget(GainButton(config, widgets, osc))
        vlayout.addWidget(ResetButton(config, osc))

        self.setLayout(vlayout)