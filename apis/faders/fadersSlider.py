import sys
import traceback
sys.path.insert(0, '../')

from apis.snippets.loadSingle import fireLine
import asyncio
from PyQt6.QtWidgets import (
    QSlider,
)

class FadersSlider(QSlider):
    def __init__(self, osc, commands, index):
        super().__init__()

        self.osc = osc
        self.commands = commands
        self.index = index

        self.setRange(0, 127)
        self.setValue(0)
        self.setSingleStep(1)
        self.setTickInterval(21)
        self.setTickPosition(QSlider.TickPosition.TicksRight)
        self.valueChanged.connect(self.slider)
    
    def slider(self):
        try:
            asyncio.run(main(self.osc, self.commands[self.index], self))
        except Exception:
            # Fail Quietly
            print(traceback.format_exc())

async def main(osc, commands, fader):
    # Command should be in following format:
    # [foh|iem] [osc command] [min float] [max float]
    for command in commands:
        components = command.split()
        faderPosition = float(fader.value()) / 127.0
        min = float(components[2])
        max = float(components[3])
        arg = (faderPosition * (max - min)) + min
        line = components[0] + " " + components[1] + " " + str(arg) + " float"
        await fireLine(osc, line, False)