import os
from PyQt6.QtGui import (
    QAction,
)
from PyQt6.QtWidgets import (
    QMessageBox,
)

class ClearCache(QAction):
    def __init__(self, s):
        super().__init__("Clear Cache", s)
        self.s = s
        self.triggered.connect(self.main)

    def main(self):
        statusCode = os.system("rm ./data/*.cache")
        
        if statusCode == 0:
            self.s.saveCache = False
            dlg = QMessageBox(self.s)
            dlg.setWindowTitle("Clear Cache")
            dlg.setText("Cache cleared. App will use default parameters on next startup.")
            dlg.exec()
        else:
            dlg = QMessageBox(self.s)
            dlg.setWindowTitle("Clear Cache")
            dlg.setText("Error Updating. Please check logs for details.")
            dlg.exec()