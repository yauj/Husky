from PyQt6.QtWidgets import (
    QDialog,
    QHBoxLayout,
    QMessageBox,
    QPushButton,
    QTextEdit,
    QVBoxLayout,
)
import traceback

class FadersEditButton(QPushButton):
    def __init__(self, osc, fader):
        super().__init__("Edit")
        self.osc = osc
        self.fader = fader
        self.pressed.connect(self.clicked)
    
    def clicked(self):
        FadersEditDialog(self.osc, self.fader).exec()
        self.setDown(False)

class FadersEditDialog(QDialog):
    def __init__(self, osc, fader):
        super().__init__()

        textbox = QTextEdit()
        textbox.setMinimumWidth(500)
        for command in fader["commands"]:
            textbox.append(command.strip())

        vlayout = QVBoxLayout()

        hlayout = QHBoxLayout()
        hlayout.addWidget(UpdateButton(osc, textbox, "Minimum"))
        hlayout.addWidget(UpdateButton(osc, textbox, "Maximum"))
        vlayout.addLayout(hlayout)

        vlayout.addWidget(textbox)
        vlayout.addWidget(EditButton(self, textbox, fader))

        self.setLayout(vlayout)

class EditButton(QPushButton):
    def __init__(self, parent, textbox, fader):
        super().__init__("Update")
        self.parent = parent
        self.textbox = textbox
        self.fader = fader
        self.pressed.connect(self.clicked)
    
    def clicked(self):
        commands = []
        for line in self.textbox.toPlainText().splitlines():
            if line.strip() != "":
                commands.append(line.strip())
        
        self.fader["commands"] = commands
            
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
        lines = []
        fohSettings = {}
        iemSettings = {}
        for line in self.textbox.toPlainText().splitlines():
            if line.strip() != "":
                lines.append(line)
                components = line.split()
                if components[0] == "foh":
                    fohSettings[components[1]] = None
                elif components[0] == "iem":
                    iemSettings[components[1]] = None
                
        fohValues = self.osc["fohClient"].bulk_send_messages(fohSettings)
        iemValues = self.osc["iemClient"].bulk_send_messages(iemSettings)

        self.textbox.clear()
        for line in lines:
            components = line.split()
            if components[0] == "midi":
                self.textbox.append(line)
            else:
                value = components[2]
                if components[0] == "foh":
                    value = fohValues[components[1]]
                elif components[0] == "iem":
                    value = iemValues[components[1]]

                if self.name == "Minimum":
                    self.textbox.append(components[0] + " " + components[1] + " " + str(value) + " " + components[3])
                if self.name == "Maximum":
                    self.textbox.append(components[0] + " " + components[1] + " " + components[2] + " " + str(value))
