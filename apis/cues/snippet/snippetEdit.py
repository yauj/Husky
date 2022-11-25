import sys
sys.path.insert(0, '../')

from PyQt6.QtWidgets import (
    QFileDialog,
    QPushButton,
)

class SnippetEditButton(QPushButton):
    def __init__(self, filename, textbox):
        super().__init__("Save Snippet")
        self.filename = filename
        self.textbox = textbox
        self.pressed.connect(self.clicked)
    
    def clicked(self):
        dlg = QFileDialog()
        dlg.setWindowTitle("Save Snippet")
        dlg.setAcceptMode(QFileDialog.AcceptMode.AcceptSave)
        dlg.setDirectory("data")
        dlg.selectFile(self.filename.text())
        dlg.setDefaultSuffix(".osc") 
        if dlg.exec():
            with open(dlg.selectedFiles()[0], "w") as file:
                for line in self.textbox.toPlainText().splitlines():
                    if line.strip() != "":
                        file.write("\n" + line.strip())

            self.filename.setText("")
            self.textbox.clear()

        self.setDown(False)