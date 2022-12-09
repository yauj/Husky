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
            cue["key"].setCurrentIndex(-1)
            cue["lead"].setCurrentIndex(-1)
            cue["snippet"].setText("")
        
        self.setDown(False)
