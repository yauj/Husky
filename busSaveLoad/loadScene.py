# Load specified Bus Settings
# Suggested that this script is run from the busSaveLoad directory

import sys
sys.path.insert(0, '../')
sys.path.insert(0, '../util')

from config import X32_IP_ADDRESS
from constants import BUSES
from glob import glob
from sceneMappers import mapOnOffToFloat, mapLevelToFloat, mapPanToFloat
from pythonosc.dispatcher import Dispatcher
from pythonosc.osc_server import BlockingOSCUDPServer
from pythonosc.udp_client import SimpleUDPClient

ODD_BUSES = ["01", "03", "05", "07", "09", "11", "13", "15"]

def printHandler(address, *args):
    print(f"{address}: {args}")

dispatcher = Dispatcher()
dispatcher.set_default_handler(printHandler)

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
    name = input("Please type the name of the person who is using Bus " + bus + ": (Type n to skip loading this Bus)\n  ")
    if (name != "n"):
        name = name.replace(" ", "")
        busNameMatches = glob("*_" + bus + "_" + name + ".scn")
        if busNameMatches:
            busNameMatches.sort(reverse=True)
            print("    Good Matches by bus and name:")
            for name in busNameMatches[:3]:
                print ("      " + name)
        
        nameMatches = glob("*_" + name + ".scn")
        nameMatches = list(set(nameMatches) - set(busNameMatches))
        if nameMatches:
            nameMatches.sort(reverse=True)
            print("    Good Matches by name:")
            for name in nameMatches[:3]:
                print ("      " + name)

        busMatches = glob("*_" + bus + "_*.scn")
        busMatches = list(set(busMatches) - set(busNameMatches))
        if busMatches:
            busMatches.sort(reverse=True)
            print("    Good Matches by bus:")
            for name in busMatches[:3]:
                print ("      " + name)
        filename = input("  Please copy in scene you want to load for Bus " + bus + ": (Type n to skip loading this Bus)\n    ")
        if (filename != "n"):
            filename.strip()
            with open(filename) as f:
                f.readline() # Skip Header Line
                while (line := f.readline().strip()):
                    compenents = line.split()
                    
                    client.send_message(compenents[0] + "/on", mapOnOffToFloat(compenents[1]))
                    client.send_message(compenents[0] + "/level", mapLevelToFloat(compenents[2]))

                    if (bus in ODD_BUSES):
                        client.send_message(compenents[0] + "/pan", mapPanToFloat(compenents[3]))
            print("  Finished loading " + filename + " settings to bus " + bus + "\n")