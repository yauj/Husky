from PyQt6.QtWidgets import (
    QCheckBox,
    QMessageBox,
    QPushButton,
)
import traceback

class TalkbackBox(QCheckBox):
    def __init__(self, config, osc, chName):
        super().__init__()
        self.config = config
        self.osc = osc
        self.chName = chName
        if self.osc["iemClient"].connected:
            self.stateChanged.connect(self.clicked)
            self.setChecked(True)
        else:
            self.setChecked(True)
            self.stateChanged.connect(self.clicked)
    
    def clicked(self, value):
        try:
            arg = 1 if value == 2 else 0
            self.osc["iemClient"].send_message("/ch/30/mix/" + self.config["personal"][self.chName]["iem_bus"] + "/on", arg)
        except Exception as ex:
            print(traceback.format_exc())
            dlg = QMessageBox(self)
            dlg.setWindowTitle("Talkback")
            dlg.setText("Error: " + str(ex))
            dlg.exec()


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