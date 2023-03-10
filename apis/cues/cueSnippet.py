from apis.cues.snippet.snippetLayer import SnippetDialog
from PyQt6.QtWidgets import (
    QPushButton,
)

class CueSnippetButton(QPushButton):
    def __init__(self, config, osc):
        super().__init__()
        self.config = config
        self.osc = osc
        self.setFilename("")

        self.pressed.connect(self.clicked)
    
    def clicked(self):
        dlg = SnippetDialog(self, self.config, self.osc)
        dlg.exec()

        self.setDown(False)
    
    def setFilename(self, filename):
        self.filename = filename
        if filename == "":
            self.setText("Attach Snippet")
            self.setStyleSheet("color: grey")
        else:
            self.setText(filename.split("/")[-1])
            self.setStyleSheet("")