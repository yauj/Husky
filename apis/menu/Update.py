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

class UpdateApp(QAction):
    def __init__(self, parent):
        super().__init__("Update App", parent)
        self.parent = parent
        self.triggered.connect(UpdateDialog(parent).exec)

class UpdateDialog(QDialog):
    def __init__(self, parent):
        super().__init__(parent)
        isApp = None
        
        if os.path.exists("pyinstaller.sh"): # In Main Directory
            isApp = False
        elif os.path.exists("../../../../pyinstaller.sh"): # In Dist Directory
            isApp = True
        else:
            vlayout = QVBoxLayout()
            label = QLabel("Unable to Update")
            label.setStyleSheet("color:red")
            vlayout.addWidget(label)
            self.setLayout(vlayout)
        
        if isApp is not None:
            vlayout = QVBoxLayout()

            vlayout.addWidget(QLabel("Update App to Latest Version"))

            hlayout = QHBoxLayout()
            hlayout.addWidget(QLabel("Version:"))
            branchName = QComboBox()
            os.system("git fetch; git branch -r > update.log") # TODO: Figure out how to timeout git fetch call
            with open("update.log") as file:
                while (line := file.readline().strip()):
                    if " -> " not in line:
                        branchName.addItem(line.replace("origin/", ""))
            os.system("git rev-parse --abbrev-ref HEAD > update.log")
            with open("update.log") as file:
                branchName.setCurrentText(file.readline().strip())
            os.system("rm update.log")
            hlayout.addWidget(branchName)
            vlayout.addLayout(hlayout)

            vlayout.addWidget(UpdateButton(parent, branchName, isApp))

            self.setLayout(vlayout)

class UpdateButton(QPushButton):
    def __init__(self, parent, branchName, isApp):
        super().__init__("Update", parent)
        self.parent = parent
        self.branchName = branchName
        self.isApp = isApp

        self.pressed.connect(self.onPressed)
    
    def onPressed(self):
        statusCode = os.system("git switch " + self.branchName.currentText())
        
        if statusCode == 0:
            dlg = QMessageBox(self.parent)
            dlg.setWindowTitle("Update App")
            dlg.setText("App Updated. Quitting App now. Please open again.")
            if dlg.exec():
                if self.isApp:
                    os.system("../../../../pyinstaller.sh")
                else:
                    os.system("./pyinstaller.sh")
                os._exit(os.EX_OK)
        else:
            dlg = QMessageBox(self.parent)
            dlg.setWindowTitle("Update App")
            dlg.setText("Error Updating. Please check logs for details: \nscreen -r Husky")
            dlg.exec()