# Load specified Bus Settings
# Suggested that this script is run from the busSaveLoad directory

import sys
sys.path.insert(0, '../')

import asyncio
from config import BUSES_TO_SAVE
from glob import glob
from loadSingleScene import runSingle
from util.constants import ALL_BUSES
from util.defaultOSC import SimpleClient, RetryingServer

async def main(client):
    server = RetryingServer()
    client._sock = server.socket

    await client.send_message("/info", None)
    server.handle_request()

    files = glob("*.scn")
    names = []
    for filename in files:
        names.append(filename.split(".")[0].split("_")[2])
    print("Names in Directory: " + str(set(names)))
    print("Buses to process: " + str(BUSES_TO_SAVE))

    for bus in BUSES_TO_SAVE:
        name = input("Please type the name of the person who is using Bus " + bus + ": (Type n to skip loading this Bus)\n  ")
        if (name != "n"):
            name = name.replace(" ", "")
            await runSingle(client, bus, name)
            
if __name__ == "__main__":
    asyncio.run(main(SimpleClient()))