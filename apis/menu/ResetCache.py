from PyQt6.QtGui import (
    QAction,
)
from PyQt6.QtWidgets import (
    QMessageBox,
)
import subprocess

class ResetCache(QAction):
    def __init__(self, s):
        super().__init__("Reset Cache", s)
        self.s = s
        self.triggered.connect(self.main)

    def main(self):
        dlg = QMessageBox(self.s)
        dlg.setWindowTitle("Reset Cache")
        dlg.setText("Are you sure you want to clear cache?\nApp will use default parameters on next startup.")
        dlg.setStandardButtons(QMessageBox.StandardButton.Ok | QMessageBox.StandardButton.Cancel)
        if dlg.exec() == QMessageBox.StandardButton.Ok:
            self.s.saveCache = False
            subprocess.Popen("rm ./data/*.cache", shell = True).wait()