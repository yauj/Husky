import sys
sys.path.insert(0, '../')

from PyQt6.QtWidgets import (
    QFileDialog,
    QPushButton,
)

class CueLoadButton(QPushButton):
    def __init__(self, cues):
        super().__init__("Load Set")
        self.cues = cues
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
                idx = 0
                while (line := file.readline().strip()):
                    components = line.split()

                    if components[0] == "N":
                        self.cues[idx]["key"].setCurrentIndex(-1)
                    else:
                        self.cues[idx]["key"].setCurrentText(components[0])

                    if components[1] == "N":
                        self.cues[idx]["lead"].setCurrentIndex(-1)
                    else:
                        self.cues[idx]["lead"].setCurrentText(components[1])

                    if components[2] == "N":
                        self.cues[idx]["snippet"].setText("")
                    else:
                        self.cues[idx]["snippet"].setText(components[2])

                    idx = idx + 1