from PyQt6.QtWidgets import (
    QPushButton,
)

from util.constants import getConfig

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

        itr = enumerate(self.config["cues"]["faders"])
        for fader in self.widgets["faders"]:
            fader["commands"] = []
            fader["slider"].setValue(0)
            try:
                _, name = itr.__next__()
                fohConfig = getConfig(self.config["cues"]["faders"][name], self.osc["fohClient"].mixerType) # Hardcoded. Might be liability in the future.
                if fohConfig is None:
                    fader["commands"] = []
                    fader["name"].setText("")
                else:
                    fader["commands"] = fohConfig["commands"]
                    fader["name"].setText(name)
                    if "defaultValue" in fohConfig:
                        fader["slider"].setValue(fohConfig["defaultValue"])
            except StopIteration:
                fader["commands"] = []
                fader["name"].setText("")
        
        for idx, fader in enumerate(self.widgets["faders"]):
            fader["slider"].refreshSubscription(prevCommands[idx], fader["commands"])

        self.setDown(False)
