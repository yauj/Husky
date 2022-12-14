from PyQt6.QtWidgets import (
    QCheckBox,
    QDialog,
    QHBoxLayout,
    QLabel,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
    QWidget,
)
import traceback
from util.lock import OwnerLock

class TalkbackButton(QPushButton):
    def __init__(self, config, osc):
        super().__init__("Modify Talkback")
        self.config = config
        self.osc = osc
        self.pressed.connect(self.clicked)
    
    def clicked(self):
        TalkbackDialog(self.config, self.osc).exec()
        self.setDown(False)

class TalkbackDialog(QDialog):
    def __init__(self, config, osc):
        super().__init__()
        vlayout = QVBoxLayout()

        label = QLabel("Specify who to talkback to. A checked box indicates that talkback is active for channel.")
        label.setMaximumHeight(20)
        vlayout.addWidget(label)
   
        self.talkbacks = {}

        vlayout.addWidget(TalkbackAllButton(osc, self.talkbacks))
        for chName in config["personal"]:
            if "iem_bus" in config["personal"][chName]:
                hlayout = QHBoxLayout()
                hlayout.addWidget(QLabel(chName + ":"))
                hlayout.addWidget(TalkbackMeButton(osc, self.talkbacks, chName))
                self.talkbacks[chName] = TalkbackBox(config, osc, chName)
                spacer = QWidget()
                spacer.setFixedWidth(30)
                hlayout.addWidget(spacer)
                hlayout.addWidget(self.talkbacks[chName])
                vlayout.addLayout(hlayout)

        self.setLayout(vlayout)

class TalkbackBox(QCheckBox):
    def __init__(self, config, osc, chName):
        super().__init__()
        self.osc = osc
        self.command = config["talkbackChannel"] + "/mix/" + config["personal"][chName]["iem_bus"] + "/on"
        self.lock = OwnerLock()
        self.setFixedWidth(20)
        self.stateChanged.connect(self.clicked)
        osc["iemServer"].subscription.add(self.command, self.processSubscription)
    
    def clicked(self, value):
        try:
            if self.lock.acquire("button"):
                arg = 1 if value == 2 else 0
                self.osc["iemClient"].send_message(self.command, arg)
        except Exception as ex:
            print(traceback.format_exc())
            dlg = QMessageBox(self)
            dlg.setWindowTitle("Talkback")
            dlg.setText("Error: " + str(ex))
            dlg.exec()
    
    def processSubscription(self, mixerName, message, arg):
        if self.lock.acquire(mixerName + " " + message):
            self.setChecked(arg == 1)

class TalkbackAllButton(QPushButton):
    def __init__(self, osc, boxes):
        super().__init__("Talk to Everybody!")
        self.osc = osc
        self.boxes = boxes
        self.pressed.connect(self.clicked)
    
    def clicked(self):
        if not self.osc["iemClient"].connected:
            dlg = QMessageBox(self)
            dlg.setWindowTitle("Talkback")
            dlg.setText("Error: Not Connected to IEM Client")
            dlg.exec()
        else:
            for name in self.boxes:
                self.boxes[name].setChecked(True)
        
        self.setDown(False)

class TalkbackMeButton(QPushButton):
    def __init__(self, osc, boxes, chName):
        super().__init__("Talk to just Me!")
        self.osc = osc
        self.boxes = boxes
        self.chName = chName
        self.pressed.connect(self.clicked)
        self.setFixedWidth(150)
    
    def clicked(self):
        if not self.osc["iemClient"].connected:
            dlg = QMessageBox(self)
            dlg.setWindowTitle("Talkback")
            dlg.setText("Error: Not Connected to IEM Client")
            dlg.exec()
        else:
            for name in self.boxes:
                if (name == self.chName):
                    self.boxes[name].setChecked(True)
                else:
                    self.boxes[name].setChecked(False)

        self.setDown(False)