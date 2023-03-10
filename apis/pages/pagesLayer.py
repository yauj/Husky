from apis.pages.pagesAutoMix import AutoMixButton
from apis.pages.pagesGain import GainButton
from apis.pages.pagesMutes import MutesButton
from apis.pages.pagesRouting import RoutingButton
from apis.pages.pagesTalkback import TalkbackButton
from PyQt6.QtWidgets import (
    QLabel,
    QVBoxLayout,
    QWidget,
)
from util.constants import MIXER_TYPE

class PagesLayer(QWidget):
    def __init__(self, config, widgets, osc):
        super().__init__()

        vlayout = QVBoxLayout()

        label = QLabel("Dialogs:")
        label.setStyleSheet("font-weight: bold")
        label.setFixedHeight(20)
        vlayout.addWidget(label)
        label = QLabel(
            "These are pages that are top level windows.\n" +
            "These pages have to be closed to operate the main window again.\n" +
            "These pages have no feedback functionality.\n" +
            "External changes will not be reflected on these pages."
        )
        label.setFixedHeight(65)
        vlayout.addWidget(label)

        vlayout.addWidget(GainButton(config, widgets, osc))
        vlayout.addWidget(MutesButton(config, osc))
        if MIXER_TYPE == "X32":
            vlayout.addWidget(RoutingButton(config, widgets, osc))

            label = QLabel("Windows:")
            label.setStyleSheet("font-weight: bold")
            label.setFixedHeight(20)
            vlayout.addWidget(label)
            label = QLabel(
                "These are pages that are new windows.\n" +
                "These pages can continue to be opened in the background.\n" +
                "These pages have feedback functionality.\n" +
                "External changes will be reflected on these pages."
            )
            label.setFixedHeight(65)
            vlayout.addWidget(label)

            vlayout.addWidget(TalkbackButton(config, widgets, osc))
            vlayout.addWidget(AutoMixButton(config, widgets, osc))

        self.setLayout(vlayout)