import os
from PyQt6.QtGui import (
    QAction,
)
from PyQt6.QtWidgets import (
    QComboBox,
    QDialog,
    QHBoxLayout,
    QLabel,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
)
import subprocess

class UpdateApp(QAction):
    def __init__(self, parent):
        super().__init__("Update App", parent)
        self.parent = parent
        self.triggered.connect(UpdateDialog(parent).exec)

class UpdateDialog(QDialog):
    def __init__(self, parent):
        super().__init__(parent)
        isApp = None
        exStr = None
        
        if os.path.exists("pyinstaller.sh"): # In Main Directory
            isApp = False
        elif os.path.exists("../../../../pyinstaller.sh"): # In Dist Directory
            isApp = True
        else:
            exStr = "Not in valid Directory. To update, app needs to be in dist/ directory of a properly set up repo."

        if exStr is None:
            try:
                subprocess.check_output("git fetch", shell = True, stderr = subprocess.STDOUT, timeout = 10.0)
            except subprocess.CalledProcessError as ex:
                exStr = ex.output.decode("utf-8")
            except subprocess.TimeoutExpired as ex:
                exStr = "Timed out waiting to fetch latest code. Check Internet Connection."
            except Exception as ex:
                exStr = str(ex)

        if exStr is None:
            vlayout = QVBoxLayout()

            vlayout.addWidget(QLabel("Update App to Latest Version"))

            vlayout.addWidget(UpdateButton(parent, isApp))

            self.setLayout(vlayout)
        else:
            vlayout = QVBoxLayout()
            label = QLabel(exStr)
            label.setStyleSheet("color:red")
            vlayout.addWidget(label)
            self.setLayout(vlayout)

class UpdateButton(QPushButton):
    def __init__(self, parent, isApp):
        super().__init__("Update (Expect this to take approx 1 minute)", parent)
        self.parent = parent
        self.isApp = isApp

        self.pressed.connect(self.onPressed)
    
    def onPressed(self):
        statusCode = os.system("git pull origin $(git rev-parse --abbrev-ref HEAD) > update.log")
        
        if statusCode == 0:
            if self.isApp:
                os.system("../../../../pyinstaller.sh")
            else:
                os.system("./pyinstaller.sh")

            dlg = QMessageBox(self.parent)
            dlg.setWindowTitle("Update App")
            dlg.setText("App Updated. Quitting App now. Please open again.")
            if dlg.exec():
                os._exit(os.EX_OK)
        else:
            dlg = QMessageBox(self.parent)
            dlg.setWindowTitle("Update App")
            dlg.setText("Error Updating. Please check logs for details.")
            dlg.exec()