from datetime import date, timedelta
from PyQt6.QtWidgets import (
    QFileDialog,
    QPushButton,
)

class SnippetCreateButton(QPushButton):
    def __init__(self, filename):
        super().__init__()
        self.filename = filename
        if self.filename.text() == "":
            self.setText("Create New Blank Snippet")
        else:
            self.setText("Clear")
        self.pressed.connect(self.clicked)
        self.setFixedWidth(300)
    
    def clicked(self):
        if self.filename.text() == "":
            # Create New File
            nextSun = (date.today() + timedelta(6 - date.today().weekday())).strftime("%Y%m%d")
            dlg = QFileDialog()
            dlg.setWindowTitle("Save Snippet")
            dlg.setAcceptMode(QFileDialog.AcceptMode.AcceptSave)
            dlg.setDirectory("data")
            dlg.selectFile(nextSun + "_CUE_SWS_?.osc")
            dlg.setDefaultSuffix(".osc") 
            if dlg.exec():
                self.filename.setText(dlg.selectedFiles()[0])
                with open(dlg.selectedFiles()[0], "w") as file:
                    file.write("") # Write header line
        else:
            self.filename.setText("")

        self.setDown(False)