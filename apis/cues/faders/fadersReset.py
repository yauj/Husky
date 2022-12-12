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
        prevFaderFirstCommands = []
        for fader in self.widgets["faders"]:
            if len(fader["commands"]) > 0:
                prevFaderFirstCommands.append(fader["commands"][0])
            else:
                prevFaderFirstCommands.append(None)

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
            if prevFaderFirstCommands[idx] is not None and len(fader["commands"]) > 0:
                fader["slider"].refreshSubscription(prevFaderFirstCommands[idx], fader["commands"][0])

        self.setDown(False)
