import os
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
                loadCue(file, self.widgets)
        
        self.setDown(False)

def loadCue(file, widgets):
    prevCommands = []
    for fader in widgets["faders"]:
        lst = []
        for command in fader["commands"]:
            lst.append(command)
        prevCommands.append(lst)

    file.readline() # Skip Header Line
    cueIdx = 0
    faderIdx = -1
    lastFaderName = None
    while (line := file.readline().strip()):
        components = line.split()

        if components[0] == "cue":
            if cueIdx < len(widgets["cues"]):
                if components[1] == "N":
                    widgets["cues"][cueIdx]["key"].setCurrentIndex(-1)
                else:
                    widgets["cues"][cueIdx]["key"].setCurrentText(components[1])

                if components[2] == "N":
                    widgets["cues"][cueIdx]["lead"].setCurrentIndex(-1)
                else:
                    widgets["cues"][cueIdx]["lead"].setCurrentText(components[2])

                if components[3] == "N":
                    widgets["cues"][cueIdx]["snippet"].setFilename("")
                else:
                    filename = " ".join(components[3:])
                    if os.path.exists(filename):
                        widgets["cues"][cueIdx]["snippet"].setFilename(filename)
                    else:
                        print("Cue Snippet File not found: " + filename)
                        widgets["cues"][cueIdx]["snippet"].setFilename("")
                cueIdx = cueIdx + 1
        elif components[0] == "fader":
            command = " ".join(components[1:5])
            name = " ".join(components[5:])
            if lastFaderName != name:
                faderIdx = faderIdx + 1
                if faderIdx < len(widgets["faders"]):
                    widgets["faders"][faderIdx]["commands"] = []
                    lastFaderName = name
            if faderIdx < len(widgets["faders"]):
                widgets["faders"][faderIdx]["name"].setText(name)
                widgets["faders"][faderIdx]["commands"].append(command)
    
    for idx, fader in enumerate(widgets["faders"]):
        fader["slider"].refreshSubscription(prevCommands[idx], fader["commands"])