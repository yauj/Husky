# Load specified Bus Settings
# Suggested that this script is run from the busSaveLoad directory

import sys
sys.path.insert(0, '../')

import asyncio
from constants import BUSES
from glob import glob
from util.defaultOSC import SimpleClient, RetryingServer
from util.sceneMappers import mapOnOffToFloat, mapLevelToFloat, mapPanToFloat

ODD_BUSES = ["01", "03", "05", "07", "09", "11", "13", "15"]

async def main(client):
    global ODD_BUSES

    server = RetryingServer()
    client._sock = server.socket

    await client.send_message("/info", None)
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
                        
                        await client.send_message(compenents[0] + "/on", mapOnOffToFloat(compenents[1]))
                        await client.send_message(compenents[0] + "/level", mapLevelToFloat(compenents[2]))

                        if (bus in ODD_BUSES):
                            await client.send_message(compenents[0] + "/pan", mapPanToFloat(compenents[3]))
                print("  Finished loading " + filename + " settings to Bus " + bus + "\n")

if __name__ == "__main__":
    asyncio.run(main(SimpleClient()))