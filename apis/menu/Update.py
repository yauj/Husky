import os
import sys
sys.path.insert(0, '../')

from PyQt6.QtGui import (
    QAction,
)
from PyQt6.QtWidgets import (
    QMessageBox,
)

class UpdateApp(QAction):
    def __init__(self, s):
        super().__init__("&Update App", s)
        self.s = s
        self.triggered.connect(self.main)

    def main(self):
        statusCode = os.system("git pull origin master > update.log")
        statusMsg = ""
        with open("update.log") as file:
            statusMsg = file.readline()
        os.system("rm update.log")
        
        if statusMsg == "Already up to date.":
            dlg = QMessageBox(self.s)
            dlg.setWindowTitle("Update App")
            dlg.setText(statusMsg)
            dlg.exec()
        elif statusCode == 0:
            dlg = QMessageBox(self.s)
            dlg.setWindowTitle("Update App")
            dlg.setText(statusMsg + " Quitting App now.")
            if dlg.exec():
                os._exit(os.EX_OK)
        else:
            dlg = QMessageBox(self.s)
            dlg.setWindowTitle("Update App")
            dlg.setText("Error Updating. Please check server.log.")
            dlg.exec()