import threading
from PyQt6.QtCore import (
    pyqtSignal,
    pyqtSlot
)
from PyQt6.QtWidgets import (
    QDialog,
    QLabel,
    QProgressBar,
    QPushButton,
    QVBoxLayout,
)

class ProgressDialog(QDialog):
    initBar = pyqtSignal(int)
    progressOne = pyqtSignal()
    complete = pyqtSignal()
    completeWithMessage = pyqtSignal(str)
    raiseException = pyqtSignal(Exception)

    def __init__(self, message, function):
        super().__init__()
        self.message = message
        self.function = function
        self.th = None

        vlayout = QVBoxLayout()
        self.label = QLabel(self.message + "ing")
        vlayout.addWidget(self.label)

        self.progressBar = QProgressBar()
        self.progressBar.setTextVisible(True)
        vlayout.addWidget(self.progressBar)

        self.okButton = QPushButton("OK")
        self.okButton.pressed.connect(self.close)
        self.okButton.setEnabled(False)
        vlayout.addWidget(self.okButton)

        self.setLayout(vlayout)

        self.initBar.connect(self.onInitBar)
        self.progressOne.connect(self.onProgressOne)
        self.complete.connect(self.onComplete)
        self.completeWithMessage.connect(self.onCompleteWithMessage)
        self.raiseException.connect(self.onRaiseException)
    
    def exec(self):
        self.th = threading.Thread(target = self.function, args = (self,))
        self.th.start()
        return super().exec()

    @pyqtSlot(int)
    def onInitBar(self, maxVal):
        self.progressBar.setRange(0, maxVal)
        self.progressBar.setValue(0)
    
    @pyqtSlot()
    def onProgressOne(self):
        self.progressBar.setValue(self.progressBar.value() + 1)

    @pyqtSlot()
    def onComplete(self):
        self.label.setText(self.message + "ed")
        self.label.setStyleSheet("color: green")
        self.okButton.setEnabled(True)
        self.progressBar.setRange(0, 1)
        self.progressBar.setValue(1)
    
    @pyqtSlot(str)
    def onCompleteWithMessage(self, message):
        self.label.setText(message)
        self.label.setStyleSheet("color: green")
        self.okButton.setEnabled(True)
        self.progressBar.setRange(0, 1)
        self.progressBar.setValue(1)

    @pyqtSlot(Exception)
    def onRaiseException(self, ex):
        self.label.setText("Error: " + str(ex))
        self.label.setStyleSheet("color: red")
        self.okButton.setEnabled(True)