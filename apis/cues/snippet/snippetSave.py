from PyQt6.QtWidgets import (
    QMessageBox,
    QPushButton,
)

class SnippetSaveButton(QPushButton):
    def __init__(self, parent, filename, textbox):
        super().__init__("Save Snippet")
        self.parent = parent
        self.filename = filename
        self.textbox = textbox
        self.pressed.connect(self.clicked)
    
    def clicked(self):
        with open(self.filename.text(), "w") as file:
            for line in self.textbox.toPlainText().splitlines():
                if line.strip() != "":
                    file.write("\n" + line.strip())

        self.parent.accept()
        dlg = QMessageBox(self)
        dlg.setWindowTitle("Save Snippet")
        dlg.setText("Snippet Settings Saved")
        dlg.exec()