import sys
import traceback
sys.path.insert(0, '../')

from apis.snippets.saveSingle import getSetting
from PyQt6.QtWidgets import (
    QDialog,
    QHBoxLayout,
    QMessageBox,
    QPushButton,
    QTextEdit,
    QVBoxLayout,
)

class FadersEditButton(QPushButton):
    def __init__(self, osc, faders, index):
        super().__init__("Edit")
        self.osc = osc
        self.faders = faders
        self.index = index
        self.pressed.connect(self.clicked)
    
    def clicked(self):
        FadersEditDialog(self.osc, self.faders, self.index).exec()
        self.setDown(False)

class FadersEditDialog(QDialog):
    def __init__(self, osc, faders, index):
        super().__init__()

        textbox = QTextEdit()
        textbox.setMinimumWidth(500)
        for command in faders[index]:
            textbox.append(command.strip())

        vlayout = QVBoxLayout()

        hlayout = QHBoxLayout()
        hlayout.addWidget(UpdateButton(osc, textbox, "Minimum"))
        hlayout.addWidget(UpdateButton(osc, textbox, "Maximum"))
        vlayout.addLayout(hlayout)

        vlayout.addWidget(textbox)
        vlayout.addWidget(EditButton(self, textbox, faders, index))

        self.setLayout(vlayout)

class EditButton(QPushButton):
    def __init__(self, parent, textbox, faders, index):
        super().__init__("Update")
        self.parent = parent
        self.textbox = textbox
        self.faders = faders
        self.index = index
        self.pressed.connect(self.clicked)
    
    def clicked(self):
        commands = []
        for line in self.textbox.toPlainText().splitlines():
            if line.strip() != "":
                commands.append(line.strip())
        
        self.faders[self.index] = commands
            
        self.parent.close()
        dlg = QMessageBox(self)
        dlg.setWindowTitle("Edit")
        dlg.setText("Fader Settings Updated")
        dlg.exec()

class UpdateButton(QPushButton):
    def __init__(self, osc, textbox, name):
        super().__init__("Update " + name)
        self.osc = osc
        self.textbox = textbox
        self.name = name
        self.pressed.connect(self.clicked)
    
    def clicked(self):
        try:
            self.main()
        except Exception as ex:
            print(traceback.format_exc())
            dlg = QMessageBox(self)
            dlg.setWindowTitle("Update")
            dlg.setText("Error: " + str(ex))
            dlg.exec()

        self.setDown(False)

    def main(self):
        commands = []
        for line in self.textbox.toPlainText().splitlines():
            if line.strip() != "":
                components = line.split()
                newLine = getSetting(components[0], self.osc[components[0] + "Client"], self.osc["server"], components[1])
                newComponents = newLine.split()
                if self.name == "Minimum":
                    commands.append(components[0] + " " + components[1] + " " + newComponents[2] + " " + components[3])
                if self.name == "Maximum":
                    commands.append(components[0] + " " + components[1] + " " + components[2] + " " + newComponents[2])
            
        self.textbox.clear()
        for command in commands:
            self.textbox.append(command)
