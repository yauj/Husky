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

class TalkbackButton(QPushButton):
    def __init__(self, config, osc):
        super().__init__("Talkback Settings")
        self.config = config
        self.osc = osc
        self.pressed.connect(self.clicked)
    
    def clicked(self):
        TalkbackDialog(self.config, self.osc).exec()
        self.setDown(False)

class TalkbackDialog(QDialog):
    def __init__(self, config, osc):
        super().__init__()
        try:
            vlayout = QVBoxLayout()

            label = QLabel("Specify who to talkback to. A checked box indicates that talkback is active for channel.")
            label.setMaximumHeight(20)
            vlayout.addWidget(label)

            initSettings = {}
            for chName in config["personal"]:
                if "iem_bus" in config["personal"][chName]:
                    initSettings[config["talkbackChannel"] + "/mix/" + config["personal"][chName]["iem_bus"] + "/on"] = None
            
                initValues = osc["iemClient"].bulk_send_messages(initSettings)

            self.talkbacks = {}

            vlayout.addWidget(TalkbackAllButton(osc, self.talkbacks))
            for chName in config["personal"]:
                if "iem_bus" in config["personal"][chName]:
                    hlayout = QHBoxLayout()
                    hlayout.addWidget(QLabel(chName + ":"))
                    hlayout.addWidget(TalkbackMeButton(osc, self.talkbacks, chName))
                    self.talkbacks[chName] = TalkbackBox(config, osc, initValues, chName)
                    spacer = QWidget()
                    spacer.setFixedWidth(30)
                    hlayout.addWidget(spacer)
                    hlayout.addWidget(self.talkbacks[chName])
                    vlayout.addLayout(hlayout)

            self.setLayout(vlayout)
        except Exception as ex:
            print(traceback.format_exc())
            vlayout = QVBoxLayout()
            label = QLabel("Error: " + str(ex))
            label.setStyleSheet("color:red")
            vlayout.addWidget(label)
            self.setLayout(vlayout)

class TalkbackBox(QCheckBox):
    def __init__(self, config, osc, initValues, chName):
        super().__init__()
        self.osc = osc
        self.command = config["talkbackChannel"] + "/mix/" + config["personal"][chName]["iem_bus"] + "/on"
        self.setFixedWidth(20)
        self.setChecked(initValues[self.command] == 1 if initValues[self.command] is not None else 1)
        self.stateChanged.connect(self.clicked)
    
    def clicked(self, value):
        try:
            arg = 1 if value == 2 else 0
            self.osc["iemClient"].send_message(self.command, arg)
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