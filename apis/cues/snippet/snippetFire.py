from apis.snippets.loadSingle import fireLines
from PyQt6.QtWidgets import (
    QMessageBox,
    QPushButton,
)
import traceback

class SnippetFireButton(QPushButton):
    def __init__(self, config, osc, textbox):
        super().__init__("Fire Commands")
        self.config = config
        self.osc = osc
        self.textbox = textbox
        self.pressed.connect(self.clicked)
    
    def clicked(self):
        try:
            main(
                self.config,
                self.osc,
                self.textbox
            )

            dlg = QMessageBox(self)
            dlg.setWindowTitle("Fire Snippet")
            dlg.setText("Fired all Commands in textbox")
            dlg.exec()
        except Exception as ex:
            print(traceback.format_exc())
            dlg = QMessageBox(self)
            dlg.setWindowTitle("Fire Snippet")
            dlg.setText("Error: " + str(ex))
            dlg.exec()

        self.setDown(False)

def main(config, osc, textbox):
    lines = []
    for line in textbox.toPlainText().splitlines():
        if line.strip() != "":
            lines.append(line)

    fireLines(config, osc, lines, False)