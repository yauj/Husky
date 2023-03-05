from PyQt6.QtGui import (
    QAction,
)
from PyQt6.QtWidgets import (
    QMessageBox,
)
import subprocess

class ClearCache(QAction):
    def __init__(self, s):
        super().__init__("Clear Cache", s)
        self.s = s
        self.triggered.connect(self.main)

    def main(self):
        dlg = QMessageBox(self.s)
        dlg.setWindowTitle("Clear Cache")
        dlg.setText("Are you sure you want to clear cache?\nApp will use default parameters on next startup.")
        if dlg.exec():
            self.s.saveCache = False
            subprocess.Popen("rm ./data/*.cache", shell = True).wait()