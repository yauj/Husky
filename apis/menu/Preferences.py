import json
from PyQt6.QtGui import (
    QAction,
)
from PyQt6.QtWidgets import (
    QDialog,
    QLabel,
    QPushButton,
    QTextEdit,
    QVBoxLayout,
)

class Preferences(QAction):
    def __init__(self, s):
        super().__init__("&Preferences", s)
        self.s = s
        self.triggered.connect(self.main)
    
    def main(self):
        dlg = PrefDialog(self.s)
        dlg.exec()

class PrefDialog(QDialog):
    def __init__(self, mainWindow):
        super().__init__()
        vlayout = QVBoxLayout()
        
        vlayout.addWidget(QLabel("Changes the config for the app.\nRequires a restart after save to load up changes."))

        self.textbox = QTextEdit()
        self.textbox.setMinimumHeight(400)
        self.textbox.setMinimumWidth(400)
        vlayout.addWidget(self.textbox)

        # Initialize Textbox
        self.textbox.append(json.dumps(mainWindow.config, indent = 4))

        vlayout.addWidget(PrefSaveButton(mainWindow, self))

        self.setLayout(vlayout)

class PrefSaveButton(QPushButton):
    def __init__(self, mainWindow, dlgWindow):
        super().__init__("Save and Quit")
        self.mainWindow = mainWindow
        self.dlgWindow = dlgWindow
        self.pressed.connect(self.clicked)
    
    def clicked(self):
        self.mainWindow.config = json.loads(self.dlgWindow.textbox.toPlainText())
        self.mainWindow.close()
        self.dlgWindow.close()
