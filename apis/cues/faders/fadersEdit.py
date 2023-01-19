import logging
from PyQt6.QtWidgets import (
    QDialog,
    QHBoxLayout,
    QMessageBox,
    QPushButton,
    QTextEdit,
    QVBoxLayout,
)
import traceback

logger = logging.getLogger(__name__)

class FadersEditButton(QPushButton):
    def __init__(self, config, osc, fader):
        super().__init__("Edit")
        self.config = config
        self.osc = osc
        self.fader = fader
        self.pressed.connect(self.clicked)
    
    def clicked(self):
        FadersEditDialog(self.config, self.osc, self.fader).exec()
        self.setDown(False)

class FadersEditDialog(QDialog):
    def __init__(self, config, osc, fader):
        super().__init__()

        textbox = QTextEdit()
        textbox.setMinimumWidth(500)
        for command in fader["commands"]:
            textbox.append(command.strip())

        vlayout = QVBoxLayout()

        hlayout = QHBoxLayout()
        hlayout.addWidget(UpdateButton(config, osc, textbox, "Minimum"))
        hlayout.addWidget(UpdateButton(config, osc, textbox, "Maximum"))
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
        
        self.fader["slider"].refreshSubscription(self.fader["commands"], commands)

        self.fader["commands"] = commands

        self.parent.accept()
        dlg = QMessageBox(self)
        dlg.setWindowTitle("Edit")
        dlg.setText("Fader Settings Updated")
        dlg.exec()

class UpdateButton(QPushButton):
    def __init__(self, config, osc, textbox, name):
        super().__init__("Update " + name)
        self.config = config
        self.osc = osc
        self.textbox = textbox
        self.name = name
        self.pressed.connect(self.clicked)
    
    def clicked(self):
        try:
            self.main()
        except Exception as ex:
            logger.error(traceback.format_exc())
            dlg = QMessageBox(self)
            dlg.setWindowTitle("Update")
            dlg.setText("Error: " + str(ex))
            dlg.exec()

        self.setDown(False)

    def main(self):
        lines = []
        settings = {"foh": {}, "iem": {}}
        for mixerName in self.config["osc"]:
            settings[mixerName] = {}
        for line in self.textbox.toPlainText().splitlines():
            if line.strip() != "":
                lines.append(line)
                components = line.split()
                if components[0] in settings:
                    settings[components[0]][components[1]] = None
        
        values = {}
        for mixerName in settings:
            if len(settings[mixerName]) > 0:
                values[mixerName] = self.osc[mixerName + "Client"].bulk_send_messages(settings[mixerName])

        self.textbox.clear()
        for line in lines:
            components = line.split()
            if components[0] in values and components[1] in values[components[0]]:
                value = values[components[0]][components[1]]

                if self.name == "Minimum":
                    self.textbox.append(components[0] + " " + components[1] + " " + str(value) + " " + components[3])
                else:
                    self.textbox.append(components[0] + " " + components[1] + " " + components[2] + " " + str(value))
            else:
                self.textbox.append(line)