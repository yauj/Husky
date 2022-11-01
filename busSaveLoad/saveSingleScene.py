# Save down current Bus Settings
# Suggested that this script is run from the busSaveLoad directory

import sys

sys.path.insert(0, '../')

import asyncio
from config import IEM_IP_ADDRESS
from datetime import date
from glob import glob
from util.constants import ALL_BUSES, ODD_BUSES, ALL_CHANNELS
from util.defaultOSC import SimpleClient, RetryingServer
from util.sceneMappers import mapFloatToOnOff, mapFloatToLevel, mapFloatToPan

async def main(client):
    today = date.today().strftime("%Y%m%d")

    server = RetryingServer()
    client._sock = server.socket

    await client.send_message("/info", None)
    server.handle_request()

    files = glob("*.scn")
    names = []
    for filename in files:
        names.append(filename.split(".")[0].split("_")[2])
    
    print("Valid Buses: " + str(ALL_BUSES))
    print("Names in Directory: " + str(set(names)))

    bus = input("Please type the Bus that you want to process:\n  ")
    bus = bus.replace(" ", "")

    name = input("Please type the name of the person who is using Bus " + bus + ":\n  ")
    name = name.replace(" ", "")
        
    await runSingle(client, server, bus, name, today)

async def runSingle(client, server, bus, name, today):
    filename = today + "_" + bus + "_" + name + ".scn"
    with open(filename, "w") as scnFile:
        scnFile.write("#4.0# \"" + filename + "\" \"\" %000000000 1")
        for channel in ALL_CHANNELS:
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
    asyncio.run(main(SimpleClient(IEM_IP_ADDRESS)))