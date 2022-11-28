import os
import sys
sys.path.insert(0, '../')

from PyQt6.QtGui import (
    QAction,
)

class UpdateApp(QAction):
    def __init__(self, s):
        super().__init__("&Update App", s)
        self.triggered.connect(self.main)

    def main(self):
        os.system("git pull origin master")

