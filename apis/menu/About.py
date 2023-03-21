from PyQt6.QtGui import (
    QAction,
)
from PyQt6.QtWidgets import (
    QMessageBox,
)
from util.constants import APP_NAME, MIXER_TYPE, VERSION

class About(QAction):
    def __init__(self, s):
        super().__init__("&About " + APP_NAME, s)
        self.s = s

        dlg = QMessageBox(self.s)
        dlg.setWindowTitle("About " + APP_NAME)
        dlg.setText("Version: " + VERSION + "; Mixer: " + MIXER_TYPE + "\nhttps://github.com/gp-seattle/Husky")

        self.triggered.connect(dlg.exec)