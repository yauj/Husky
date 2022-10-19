# Save down current Bus Settings
# Suggested that this script is run from the busSaveLoad directory

import sys

sys.path.insert(0, '../')

import asyncio
from config import BUSES_TO_SAVE
from datetime import date
from glob import glob
from saveSingleScene import runSingle
from util.defaultOSC import SimpleClient, RetryingServer

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
    print("Buses to process: " + str(BUSES_TO_SAVE))

    for bus in BUSES_TO_SAVE:
        name = input("Please type the name of the person who used Bus " + bus + ": (Type n to skip saving this Bus)\n  ")
        if (name != "n"):
            name = name.replace(" ", "")
            await runSingle(client, server, bus, name, today)

if __name__ == "__main__":
    asyncio.run(main(SimpleClient()))