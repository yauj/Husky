from PyQt6.QtWidgets import (
    QPushButton,
)

class CueClearButton(QPushButton):
    def __init__(self, widgets):
        super().__init__("Clear All")
        self.widgets = widgets
        self.pressed.connect(self.clicked)
        self.setFixedWidth(100)
    
    def clicked(self):
        for cue in self.widgets["cues"]:
            for category in cue:
                if category == "snippet":
                    cue["snippet"].setFilename("")
                else:
                    cue[category].setCurrentIndex(-1)
        
        self.setDown(False)
