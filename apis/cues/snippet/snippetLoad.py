from PyQt6.QtWidgets import (
    QFileDialog,
    QPushButton,
)

class SnippetLoadButton(QPushButton):
    def __init__(self, filename, textbox):
        super().__init__("Load Snippet")
        self.filename = filename
        self.textbox = textbox
        self.pressed.connect(self.clicked)
    
    def clicked(self):
        dlg = QFileDialog()
        dlg.setWindowTitle("Load Set")
        dlg.setAcceptMode(QFileDialog.AcceptMode.AcceptOpen)
        dlg.setDirectory("data")
        dlg.setNameFilter("*.osc")
        if dlg.exec():
            with open(dlg.selectedFiles()[0]) as file:
                file.readline() # Skip Header Line
                self.textbox.clear() # Clear Textbox

                while (line := file.readline().strip()):
                    self.textbox.append(line)
            
            self.filename.setText(dlg.selectedFiles()[0].split("/")[-1])
        
        self.setDown(False)