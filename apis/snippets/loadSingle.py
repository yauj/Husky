import mido
import os.path
from PyQt6.QtWidgets import (
    QMessageBox,
    QPushButton,
)
import traceback
from util.customWidgets import ProgressDialog

class LoadButton(QPushButton):
    def __init__(self, config, osc, chName, filename, person):
        super().__init__("Load")
        self.config = config
        self.osc = osc
        self.chName = chName
        self.filename = filename
        self.person = person
        self.pressed.connect(self.clicked)
        self.setFixedWidth(80)

    def clicked(self):
        if (self.filename.currentText() != "" and os.path.exists("data/" + self.filename.currentText())):
            dlg = ProgressDialog("Settings for " + self.chName + " Load", self.main)
            dlg.exec()
        else:
            dlg = QMessageBox(self)
            dlg.setWindowTitle("Load")
            dlg.setText("Invalid Filename for " + self.chName)
            dlg.exec()
        
        self.setDown(False)
        
    def main(self, dlg):
        try:
            dlg.initBar.emit(loadSingleNumSettings(self.filename.currentText(), True))
            runSingle(self.config, self.osc, "data/" + self.filename.currentText(), True, dlg)
            self.person.setCurrentText(self.filename.currentText().split(".")[0].split("_")[2])
            dlg.complete.emit()
        except Exception as ex:
            print(traceback.format_exc())
            dlg.raiseException.emit(ex)

def runSingle(config, osc, filename, iemCopy, dlg = None):
    lines = []
    with open(filename) as scnFile:
        scnFile.readline() # Skip Header Line
        while (line := scnFile.readline().strip()):
            lines.append(line)
        
    fireLines(config, osc, lines, iemCopy, dlg)

    print("Loaded " + filename)

def fireLines(config, osc, lines, iemCopy, dlg = None):
    fohSettings = {}
    iemSettings = {}
    for line in lines:
        components = line.split()

        if components[0] == "midi":
            channel = int(components[2]) - 1
            control = int(components[3])
            value = int(components[4])
            if components[1] in config["midi"]:
                if config["midi"][components[1]]["type"] == "control_change":
                    osc[components[1] + "Midi"].send(mido.Message("control_change", channel = channel, control = control, value = value))
                elif config["midi"][components[1]]["type"] == "note":
                    if value == 0:
                        osc[components[1] + "Midi"].send(mido.Message("note_off", channel = channel, note = control))
                    else:
                        osc[components[1] + "Midi"].send(mido.Message("note_on", channel = channel, note = control))
        else:
            arg = " ".join(components[3:])
            if (components[2] == "int"):
                arg = int(arg)
            elif (components[2] == "float"):
                arg = float(arg)

            if (components[0] == "foh"):
                fohSettings[components[1]] = arg
                if iemCopy: # Whether not to send setting to IEM mixer as well
                    iemSettings[components[1]] = arg
            elif (components[0] == "iem"):
                iemSettings[components[1]] = arg

    if len(fohSettings) > 0:
        osc["fohClient"].bulk_send_messages(fohSettings, dlg)

    if len(iemSettings) > 0:
        osc["iemClient"].bulk_send_messages(iemSettings, dlg)

def loadSingleNumSettings(filename, iemCopy):
    num = 0
    if (os.path.exists("data/" + filename)):
        with open("data/" + filename) as file:
            file.readline() # Skip Header Line
            while (line := file.readline().strip()):
                components = line.split()

                if (components[0] == "foh"):
                    if iemCopy:
                        num = num + 2
                    else:
                        num = num + 1
                elif (components[0] == "iem"):
                    num = num + 1
    return num
