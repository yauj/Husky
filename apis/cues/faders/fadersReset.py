from PyQt6.QtWidgets import (
    QPushButton,
)

class FadersResetButton(QPushButton):
    def __init__(self, config, widgets):
        super().__init__("Reset")
        self.config = config
        self.widgets = widgets
        self.pressed.connect(self.clicked)
        self.setFixedWidth(100)
    
    def clicked(self):
        prevCommands = []
        for fader in self.widgets["faders"]:
            lst = []
            for command in fader["commands"]:
                lst.append(command)
            prevCommands.append(lst)

        itr = enumerate(self.config["faders"])
        for fader in self.widgets["faders"]:
            fader["commands"] = []
            fader["slider"].setValue(0)
            try:
                _, name = itr.__next__()
                fader["commands"] = self.config["faders"][name]["commands"]
                fader["name"].setText(name)
                if ("defaultValue" in self.config["faders"][name]):
                    fader["slider"].setValue(self.config["faders"][name]["defaultValue"])
            except StopIteration:
                fader["commands"] = []
                fader["name"].setText("")
        
        for idx, fader in enumerate(self.widgets["faders"]):
            fader["slider"].refreshSubscription(prevCommands[idx], fader["commands"])

        self.setDown(False)
