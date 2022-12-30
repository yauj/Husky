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

from util.constants import formatBus, getConfig

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

            self.talkbacks = {}
            vlayout.addWidget(TalkbackAllButton(osc, self.talkbacks))

            if "iem" not in config["osc"]:
                if "talkbackDestination" not in config:
                    raise KeyError("talkbackDestination is not specified in config.py")

                command = "/config/talk/" + config["talkbackDestination"] + "/destmap"
                self.bitmap = ["0"] * 18
                val = osc["iemClient"].bulk_send_messages({command: None})
                binVal = bin(val[command])[2:]
                for idx, x in enumerate(binVal):
                    self.bitmap[idx + (18 - len(binVal))] = x

                for chName in config["personal"]:
                    iemConfig = getConfig(config["personal"][chName], osc["iemClient"].mixerType)
                    if iemConfig is not None and "iem_bus" in iemConfig:
                        hlayout = QHBoxLayout()
                        hlayout.addWidget(QLabel(chName + ":"))
                        hlayout.addWidget(TalkbackMeButton(osc, self.talkbacks, chName))
                        self.talkbacks[chName] = TalkbackOneBox(iemConfig, osc, self.bitmap, command)
                        spacer = QWidget()
                        spacer.setFixedWidth(30)
                        hlayout.addWidget(spacer)
                        hlayout.addWidget(self.talkbacks[chName])
                        vlayout.addLayout(hlayout)
            else:
                if "talkbackChannel" not in config:
                    raise KeyError("talkbackChannel is not specified in config.py")

                initSettings = {}
                for chName in config["personal"]:
                    iemConfig = getConfig(config["personal"][chName], osc["iemClient"].mixerType)
                    if iemConfig is not None and "iem_bus" in iemConfig:
                        initSettings[config["talkbackChannel"] + "/mix/" + formatBus(iemConfig["iem_bus"], osc["iemClient"].mixerType) + "/on"] = None
                
                initValues = osc["iemClient"].bulk_send_messages(initSettings)

                for chName in config["personal"]:
                    iemConfig = getConfig(config["personal"][chName], osc["iemClient"].mixerType)
                    if iemConfig is not None and "iem_bus" in iemConfig:
                        hlayout = QHBoxLayout()
                        hlayout.addWidget(QLabel(chName + ":"))
                        hlayout.addWidget(TalkbackMeButton(osc, self.talkbacks, chName))
                        self.talkbacks[chName] = TalkbackTwoBox(iemConfig, osc, initValues)
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

# 1 Mixer
class TalkbackOneBox(QCheckBox):
    def __init__(self, config, osc, bitmap, command):
        super().__init__()
        self.osc = osc
        self.bitmap = bitmap
        self.index = 18 - int(config["iem_bus"])
        self.command = command
        self.setFixedWidth(20)
        self.setChecked(self.bitmap[self.index] == "1")
        self.stateChanged.connect(self.clicked)
    
    def clicked(self, value):
        try:
            self.bitmap[self.index] = "1" if value == 2 else "0"
            self.osc["fohClient"].send_message(self.command, int("".join(self.bitmap), 2))
        except Exception as ex:
            print(traceback.format_exc())
            dlg = QMessageBox(self)
            dlg.setWindowTitle("Talkback")
            dlg.setText("Error: " + str(ex))
            dlg.exec()

# 2 Mixers
class TalkbackTwoBox(QCheckBox):
    def __init__(self, config, osc, initValues):
        super().__init__()
        self.osc = osc
        self.command = config["talkbackChannel"] + "/mix/" + formatBus(config["iem_bus"], osc["iemClient"].mixerType) + "/on"
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
        for name in self.boxes:
            if (name == self.chName):
                self.boxes[name].setChecked(True)
            else:
                self.boxes[name].setChecked(False)

        self.setDown(False)