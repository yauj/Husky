from apis.snippets.loadAll import LoadAllButton
from apis.snippets.loadSingle import LoadButton
from apis.snippets.saveAll import SaveAllButton
from apis.snippets.saveSingle import SaveButton
import os
from PyQt6.QtWidgets import (
    QComboBox,
    QHBoxLayout,
    QLabel,
    QScrollArea,
    QTabWidget,
    QVBoxLayout,
    QWidget,
)

class SnippetsLayer(QTabWidget):
    def __init__(self, config, widgets, osc):
        super().__init__()
        self.config = config
        self.widgets = widgets
        self.osc = osc

        # Need to compile saveLayer first, since loadLayer is dependent on saveLayer
        self.addTab(self.saveLayer(), "Save")
        self.addTab(self.loadLayer(), "Load")

    def loadLayer(self):
        layout = QVBoxLayout()

        label = QLabel(
            "Enter filename in textbox.\n"
            + "Leave textbox blank if you don't want to load."
        )
        label.setFixedHeight(30)
        layout.addWidget(label)

        vlayout = QVBoxLayout()
        filenames = {}
        for chName in self.config["personal"]:
            hlayout = QHBoxLayout()

            label = QLabel(chName + ":")
            label.setFixedWidth(100)
            hlayout.addWidget(label)

            files = []
            for filename in os.listdir("data"):
                try:
                    if filename.split(".")[0].split("_")[1] == chName:
                        files.append(filename)
                except IndexError:
                    pass
            files.sort(reverse=True)

            filenames[chName] = QComboBox()
            filenames[chName].addItems(files)
            filenames[chName].setEditable(True)
            filenames[chName].setMaxCount(10)
            filenames[chName].setCurrentIndex(-1)
            hlayout.addWidget(filenames[chName])

            hlayout.addWidget(LoadButton(self.config, self.osc, chName, filenames[chName], self.widgets["personal"][chName]))

            vlayout.addLayout(hlayout)

        # Mains
        hlayout = QHBoxLayout()
        label = QLabel("Mains L/R:")
        label.setFixedWidth(100)
        hlayout.addWidget(label)
        files = []
        for filename in os.listdir("data"):
            try:
                if filename.split(".")[0].split("_")[1] == "Mains":
                    files.append(filename)
            except IndexError:
                pass
        files.sort(reverse=True)
        filenames["Mains"] = QComboBox()
        filenames["Mains"].addItems(files)
        filenames["Mains"].setEditable(True)
        filenames["Mains"].setMaxCount(10)
        filenames["Mains"].setCurrentIndex(-1)
        hlayout.addWidget(filenames["Mains"])
        hlayout.addWidget(LoadButton(self.config, self.osc, "Mains", filenames["Mains"], self.widgets["personal"]["Mains"]))
        vlayout.addLayout(hlayout)

        scrollWidget = QWidget()
        scrollWidget.setLayout(vlayout)

        scroll = QScrollArea()
        scroll.setWidget(scrollWidget)
        scroll.setWidgetResizable(True)
        
        layout.addWidget(scroll)
        layout.addWidget(LoadAllButton(self.config, self.osc, filenames, self.widgets["personal"]))
        widget = QWidget()
        widget.setLayout(layout)
        return widget

    def saveLayer(self):
        layout = QVBoxLayout()

        label = QLabel(
            "Enter name of person in textbox in the following format: 'FirstnameLastname'.\n"
            + "Leave textbox blank if you don't want to save."
        )
        label.setFixedHeight(30)
        layout.addWidget(label)

        vlayout = QVBoxLayout()
        for chName in self.config["personal"]:
            hlayout = QHBoxLayout()

            label = QLabel(chName + ":")
            label.setFixedWidth(100)
            hlayout.addWidget(label)

            names = []
            for filename in os.listdir("data"):
                try:
                    components = filename.split(".")[0].split("_")
                    if components[1] == chName:
                        names.append(components[2])
                except IndexError:
                    pass
            names = list(set(names))
            names.sort()

            self.widgets["personal"][chName] = QComboBox()
            self.widgets["personal"][chName].addItems(names)
            self.widgets["personal"][chName].setEditable(True)
            self.widgets["personal"][chName].setMaxCount(10)
            self.widgets["personal"][chName].setCurrentIndex(-1)
            hlayout.addWidget(self.widgets["personal"][chName])

            hlayout.addWidget(SaveButton(self.osc, chName, self.widgets["personal"][chName], self.config))

            vlayout.addLayout(hlayout)

        # Main L/R
        hlayout = QHBoxLayout()
        label = QLabel("Mains L/R:")
        label.setFixedWidth(100)
        hlayout.addWidget(label)
        names = []
        for filename in os.listdir("data"):
            try:
                components = filename.split(".")[0].split("_")
                if components[1] == "Mains":
                    names.append(components[2])
            except IndexError:
                pass
        names = list(set(names))
        names.sort()
        self.widgets["personal"]["Mains"] = QComboBox()
        self.widgets["personal"]["Mains"].addItems(names)
        self.widgets["personal"]["Mains"].setEditable(True)
        self.widgets["personal"]["Mains"].setMaxCount(10)
        self.widgets["personal"]["Mains"].setCurrentIndex(-1)
        hlayout.addWidget(self.widgets["personal"]["Mains"])
        hlayout.addWidget(SaveButton(self.osc, "Mains", self.widgets["personal"]["Mains"], True))
        vlayout.addLayout(hlayout)


        scrollWidget = QWidget()
        scrollWidget.setLayout(vlayout)

        scroll = QScrollArea()
        scroll.setWidget(scrollWidget)
        scroll.setWidgetResizable(True)
        
        layout.addWidget(scroll)
        layout.addWidget(SaveAllButton(self.osc, self.widgets["personal"], self.config))
        widget = QWidget()
        widget.setLayout(layout)
        return widget