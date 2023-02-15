from datetime import date
from PyQt6.QtGui import (
    QAction,
)
from PyQt6.QtWidgets import (
    QFileDialog,
)
from uuid import uuid4
import shutil

class BackupDirectory(QAction):
    def __init__(self, s):
        super().__init__("Backup Directory", s)
        self.s = s
        self.triggered.connect(self.main)

    def main(self):
        today = date.today().strftime("%Y%m%d")

        dlg = QFileDialog()
        dlg.setWindowTitle("Backup Directory")
        dlg.setAcceptMode(QFileDialog.AcceptMode.AcceptSave)
        dlg.setDirectory("~/Documents")
        dlg.selectFile(today + "_HuskyBackup.zip")
        dlg.setDefaultSuffix(".zip")
        if dlg.exec():
            shutil.make_archive(dlg.selectedFiles()[0].split(".")[0], "zip", "data")

class LoadDirectory(QAction):
    def __init__(self, s):
        super().__init__("Load Directory", s)
        self.s = s
        self.triggered.connect(self.main)

    def main(self):
        dlg = QFileDialog()
        dlg.setWindowTitle("Load Directory")
        dlg.setAcceptMode(QFileDialog.AcceptMode.AcceptOpen)
        dlg.setDirectory("~/Documents")
        dlg.setNameFilter("*.zip")
        if dlg.exec():
            tmpDir = "/tmp/" + str(uuid4())
            shutil.unpack_archive(dlg.selectedFiles()[0], tmpDir, "zip")
            shutil.copytree(tmpDir, "data", dirs_exist_ok = True)
            shutil.rmtree(tmpDir)