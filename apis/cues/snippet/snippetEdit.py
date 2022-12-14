from apis.cues.snippet.snippetAdd import SnippetAddButton
from apis.cues.snippet.snippetFire import SnippetFireButton
from apis.cues.snippet.snippetSave import SnippetSaveButton
from apis.cues.snippet.snippetUpdate import SnippetUpdateButton
import os
from PyQt6.QtWidgets import (
    QDialog,
    QHBoxLayout,
    QPushButton,
    QTextEdit,
    QVBoxLayout,
)

class SnippetEditButton(QPushButton):
    def __init__(self, config, osc, filename):
        super().__init__("Edit Current Snippet")
        self.config = config
        self.osc = osc
        self.filename = filename
        self.setEnabled(self.filename.text() != "")
        self.pressed.connect(self.clicked)
    
    def clicked(self):
        dlg = SnippetEditDialog(self.config, self.osc, self.filename)
        dlg.exec()

        self.setDown(False)

class SnippetEditDialog(QDialog):
    def __init__(self, config, osc, filename):
        super().__init__()
        self.config = config
        self.osc = osc
        self.filename = filename

        vlayout = QVBoxLayout()

        textbox = QTextEdit()
        textbox.setMinimumHeight(360)
        vlayout.addWidget(textbox)

        hlayout = QHBoxLayout()
        hlayout.addWidget(SnippetAddButton(self.config, self.osc, textbox))
        hlayout.addWidget(SnippetUpdateButton(self.osc, textbox))
        hlayout.addWidget(SnippetFireButton(self.config, self.osc, textbox))
        vlayout.addLayout(hlayout)

        vlayout.addWidget(SnippetSaveButton(self, self.filename, textbox))

        self.setLayout(vlayout)

        # Initialize Textbox if Filename is valid
        if (os.path.exists(filename.text())):
            with open(filename.text()) as file:
                file.readline() # Skip Header Line
                while (line := file.readline().strip()):
                    textbox.append(line)