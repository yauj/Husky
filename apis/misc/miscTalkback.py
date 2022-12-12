from PyQt6.QtWidgets import (
    QCheckBox,
    QMessageBox,
    QPushButton,
)
import traceback
from util.lock import OwnerLock

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