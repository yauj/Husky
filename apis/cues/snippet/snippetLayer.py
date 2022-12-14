from apis.cues.snippet.snippetCreate import SnippetCreateButton
from apis.cues.snippet.snippetEdit import SnippetEditButton
from apis.cues.snippet.snippetLoad import SnippetLoadButton
from PyQt6.QtWidgets import (
    QDialog,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QVBoxLayout,
)

class SnippetDialog(QDialog):
    def __init__(self, parent, osc):
        super().__init__()
        self.parent = parent
        self.osc = osc

        vlayout = QVBoxLayout()

        vlayout.addWidget(QLabel("Attach Snippet to Cue, so that snippet is fired when cue is fired."))
        
        hlayout = QHBoxLayout()
        hlayout.addWidget(QLabel("Filename: "))
        filename = QLineEdit(self.parent.filename)
        filename.setReadOnly(True)
        filename.textChanged.connect(self.mapFilename)
        hlayout.addWidget(filename)
        vlayout.addLayout(hlayout)

        hlayout = QHBoxLayout()
        hlayout.addWidget(SnippetLoadButton(filename))
        self.createButton = SnippetCreateButton(filename)
        hlayout.addWidget(self.createButton)
        vlayout.addLayout(hlayout)

        self.editButton = SnippetEditButton(self.osc, filename)
        vlayout.addWidget(self.editButton)

        self.setLayout(vlayout)
    
    def mapFilename(self, text):
        self.parent.setFilename(text)
        if text == "":
            self.createButton.setText("Create New Blank Snippet")
            self.editButton.setEnabled(False)
        else:
            self.createButton.setText("Clear")
            self.editButton.setEnabled(True)