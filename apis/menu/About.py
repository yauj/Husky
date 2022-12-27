from PyQt6.QtGui import (
    QAction,
)
from PyQt6.QtWidgets import (
    QMessageBox,
)
from util.constants import MIXER_TYPE, VERSION

class About(QAction):
    def __init__(self, s):
        super().__init__("&About Husky", s)
        self.s = s

        dlg = QMessageBox(self.s)
        dlg.setWindowTitle("About Husky")
        dlg.setText("Version: " + VERSION + "; Mixer: " + MIXER_TYPE)

        self.triggered.connect(dlg.exec)