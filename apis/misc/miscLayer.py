from apis.misc.miscReset import ResetButton
from apis.misc.miscTalkback import TalkbackAllButton, TalkbackBox, TalkbackMeButton
from apis.misc.miscTransfer import TransferButton
from PyQt6.QtWidgets import (
    QHBoxLayout,
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
        self.addTab(self.talkbackLayer(), "Talkback")
        self.addTab(self.resetLayer(), "Reset")
        
    def transferLayer(self):
        vlayout = QVBoxLayout()

        vlayout.addWidget(QLabel("Do you want to transfer Channel EQ, Compression, Mute settings from the FOH Mixer to the IEM Mixer?"))
        vlayout.addWidget(TransferButton(self.osc))

        widget = QWidget()
        widget.setLayout(vlayout)
        return widget

    def talkbackLayer(self):
        vlayout = QVBoxLayout()

        label = QLabel("Specify who to talkback to. A checked box indicates that talkback is active for channel.")
        label.setMaximumHeight(20)
        vlayout.addWidget(label)
   
        self.talkbacks = {}

        vlayout.addWidget(TalkbackAllButton(self.osc, self.talkbacks))
        for chName in self.config["personal"]:
            if "iem_bus" in self.config["personal"][chName]:
                hlayout = QHBoxLayout()
                hlayout.addWidget(QLabel(chName + ":"))
                hlayout.addWidget(TalkbackMeButton(self.osc, self.talkbacks, chName))
                self.talkbacks[chName] = TalkbackBox(self.config, self.osc, chName)
                spacer = QWidget()
                spacer.setFixedWidth(30)
                hlayout.addWidget(spacer)
                hlayout.addWidget(self.talkbacks[chName])
                vlayout.addLayout(hlayout)

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