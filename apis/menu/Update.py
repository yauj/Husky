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
        os.system("date > server.log")
        if os.system("git pull origin master > server.log") == 0:
            dlg = QMessageBox(self.s)
            dlg.setWindowTitle("Update App")
            dlg.setText("App Updated! Please restart App now.")
            if dlg.exec():
                os._exit(os.EX_OK)
        else:
            dlg = QMessageBox(self.s)
            dlg.setWindowTitle("Update App")
            dlg.setText("Error Updating. Please check server.log.")
            dlg.exec()

