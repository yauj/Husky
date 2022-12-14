from PyQt6.QtWidgets import (
    QFileDialog,
    QPushButton,
)

class SnippetLoadButton(QPushButton):
    def __init__(self, filename):
        super().__init__("Load Existing Snippet")
        self.filename = filename
        self.pressed.connect(self.clicked)
        self.setFixedWidth(300)

    def clicked(self):
        dlg = QFileDialog()
        dlg.setWindowTitle("Load Existing Snippet")
        dlg.setAcceptMode(QFileDialog.AcceptMode.AcceptOpen)
        dlg.setDirectory("data")
        dlg.setDefaultSuffix(".osc")
        if dlg.exec():
            self.filename.setText(dlg.selectedFiles()[0])
        
        self.setDown(False)