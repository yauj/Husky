import sys
sys.path.insert(0, '../')

from PyQt6.QtWidgets import (
    QFileDialog,
    QPushButton,
)

class CueLoadButton(QPushButton):
    def __init__(self, widgets):
        super().__init__("Load Set")
        self.widgets = widgets
        self.pressed.connect(self.clicked)
    
    def clicked(self):
        dlg = QFileDialog()
        dlg.setWindowTitle("Load Set")
        dlg.setAcceptMode(QFileDialog.AcceptMode.AcceptOpen)
        dlg.setDirectory("data")
        dlg.setNameFilter("*.cue")
        if dlg.exec():
            with open(dlg.selectedFiles()[0]) as file:
                file.readline() # Skip Header Line
                cueIdx = 0
                faderIdx = -1
                lastFaderName = None
                while (line := file.readline().strip()):
                    components = line.split()

                    if components[0] == "cue":
                        if components[1] == "N":
                            self.widgets["cues"][cueIdx]["key"].setCurrentIndex(-1)
                        else:
                            self.widgets["cues"][cueIdx]["key"].setCurrentText(components[1])

                        if components[2] == "N":
                            self.widgets["cues"][cueIdx]["lead"].setCurrentIndex(-1)
                        else:
                            self.widgets["cues"][cueIdx]["lead"].setCurrentText(components[2])

                        if components[3] == "N":
                            self.widgets["cues"][cueIdx]["snippet"].setText("")
                        else:
                            self.widgets["cues"][cueIdx]["snippet"].setText(components[3])

                        cueIdx = cueIdx + 1
                    elif components[0] == "fader":
                        command = " ".join(components[1:5])
                        name = " ".join(components[5:])
                        if lastFaderName != name:
                            faderIdx = faderIdx + 1
                            self.widgets["faders"][faderIdx]["commands"] = []
                            lastFaderName = name
                        self.widgets["faders"][faderIdx]["name"].setText(name)
                        self.widgets["faders"][faderIdx]["commands"].append(command)
        
        self.setDown(False)