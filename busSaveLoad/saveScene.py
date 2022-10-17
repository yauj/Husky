# Save down current Bus Settings
# Suggested that this script is run from the busSaveLoad directory

import sys
sys.path.insert(0, '../')
sys.path.insert(0, '../util') 

from config import X32_IP_ADDRESS
from constants import BUSES, CHANNELS
from datetime import date
from glob import glob
from sceneMappers import mapFloatToOnOff, mapFloatToLevel, mapFloatToPan
from pythonosc.dispatcher import Dispatcher
from pythonosc.osc_server import BlockingOSCUDPServer
from pythonosc.udp_client import SimpleUDPClient

ODD_BUSES = ["01", "03", "05", "07", "09", "11", "13", "15"]

today = date.today().strftime("%Y%m%d")

def printHandler(address, *args):
    print(f"{address}: {args}")

lastVal: float # List of all incoming args[0]
def listHandler(address, *args):
    global lastVal
    lastVal = args[0]

dispatcher = Dispatcher()
dispatcher.map("/info", printHandler)
dispatcher.set_default_handler(listHandler)

client = SimpleUDPClient(X32_IP_ADDRESS, 10023)
server = BlockingOSCUDPServer(("0.0.0.0", 10023), dispatcher)
client._sock = server.socket

client.send_message("/info", "")
server.handle_request()

files = glob("*.scn")
names = []
for filename in files:
    names.append(filename.split(".")[0].split("_")[2])
print("Names in Directory: " + str(set(names)))
print("Buses to process: " + str(BUSES))

for bus in BUSES:
    name = input("Please type the name of the person who used Bus " + bus + ": (Type n to skip saving this Bus)\n  ")
    if (name != "n"):
        name = name.replace(" ", "")
        filename = today + "_" + bus + "_" + name + ".scn"
        with open(filename, "w") as scnFile:
            scnFile.write("#4.0# \"" + filename + "\" \"\" %000000000 1\n")
            for channel in CHANNELS:
                line = channel + "/mix/" + bus
                client.send_message(channel + "/mix/" + bus + "/on", None)
                server.handle_request()
                line += " " + mapFloatToOnOff(lastVal)

                client.send_message(channel + "/mix/" + bus + "/level", None)
                server.handle_request()
                line += " " + mapFloatToLevel(lastVal)

                if bus in ODD_BUSES:
                    client.send_message(channel + "/mix/" + bus + "/pan", None)
                    server.handle_request()
                    line += " " + mapFloatToPan(lastVal)

                scnFile.write(line + "\n")
        print("  Created " + filename + " for settings that were read from " + bus + "\n")