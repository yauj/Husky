# Save down current Bus Settings
# Suggested that this script is run from the busSaveLoad directory

import sys
sys.path.insert(0, '../')

import asyncio
from constants import BUSES, CHANNELS
from datetime import date
from glob import glob
from util.defaultOSC import SimpleClient, RetryingServer
from util.sceneMappers import mapFloatToOnOff, mapFloatToLevel, mapFloatToPan

ODD_BUSES = ["01", "03", "05", "07", "09", "11", "13", "15"]

async def main(client):
    global ODD_BUSES

    today = date.today().strftime("%Y%m%d")

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
        name = input("Please type the name of the person who used Bus " + bus + ": (Type n to skip saving this Bus)\n  ")
        if (name != "n"):
            name = name.replace(" ", "")
            filename = today + "_" + bus + "_" + name + ".scn"
            with open(filename, "w") as scnFile:
                scnFile.write("#4.0# \"" + filename + "\" \"\" %000000000 1")
                for channel in CHANNELS:
                    prefix = channel + "/mix/" + bus
                    line = prefix
                    await client.send_message(prefix + "/on", None)
                    server.handle_request()
                    line += " " + mapFloatToOnOff(server.lastVal)

                    await client.send_message(prefix + "/level", None)
                    server.handle_request()
                    line += " " + mapFloatToLevel(server.lastVal)

                    if bus in ODD_BUSES:
                        await client.send_message(prefix + "/pan", None)
                        server.handle_request()
                        line += " " + mapFloatToPan(server.lastVal)

                    scnFile.write("\n" + line)
            print("  Created " + filename + " for settings that were read from Bus " + bus + "\n")

if __name__ == "__main__":
    asyncio.run(main(SimpleClient()))