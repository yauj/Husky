from PyQt6.QtWidgets import (
    QFileDialog,
    QPushButton,
)

class SnippetSaveButton(QPushButton):
    def __init__(self, parent, filename, headerLine, textbox):
        super().__init__("Save Snippet")
        self.parent = parent
        self.filename = filename
        self.headerLine = headerLine
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
                # Write Header
                tags = {}
                for pair in self.headerLine.split()[1:]:
                    keyVal = pair.split("=")
                    tags[keyVal[1]] = keyVal[0]
                file.write(self.headerLine)

                for line in self.textbox.toPlainText().splitlines():
                    if line.strip() != "":
                        line = line.strip()
                        for key in tags:
                            line = line.replace(key, tags[key])

                        file.write("\n" + line)

            self.filename.setText(dlg.selectedFiles()[0])

            self.parent.accept()