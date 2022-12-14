from apis.cues.snippet.snippetLayer import SnippetDialog
from PyQt6.QtWidgets import (
    QPushButton,
)

class CueSnippetButton(QPushButton):
    def __init__(self, osc):
        super().__init__("Attach Snippet")
        self.setStyleSheet("color: grey")
        self.filename = ""
        self.osc = osc

        self.pressed.connect(self.clicked)
    
    def clicked(self):
        dlg = SnippetDialog(self, self.osc)
        dlg.exec()

        self.setDown(False)