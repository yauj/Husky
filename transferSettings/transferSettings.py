# Transfer 
import sys
sys.path.insert(0, '../')

import asyncio
from config import FOH_IP_ADDRESS, IEM_IP_ADDRESS
from util.constants import COPY_CHANNELS, LINK_CHANNELS
from util.defaultOSC import SimpleClient, RetryingServer

async def main(fohClient, iemClient):
    server = RetryingServer()
    fohClient._sock = server.socket

    await fohClient.send_message("/info", None)
    server.handle_request()

    # Copy Channel Links
    for chlink in LINK_CHANNELS:
        await transferSetting(fohClient, iemClient, server, "/config/chlink/" + chlink)

    for channel in COPY_CHANNELS:
        # Copy Channel Labeling (except FOH talkback)
        for param in ["name", "icon", "color"]:
            await transferSetting(fohClient, iemClient, server, channel + "/config/" + param) 

        # Copy Low Cut
        for param in ["hpon", "hpf"]:
            await transferSetting(fohClient, iemClient, server, channel + "/preamp/" + param)

        # Copy EQ Settings
        for band in ["1", "2", "3", "4"]:
            for param in ["type", "f", "g", "q"]:
                await transferSetting(fohClient, iemClient, server, channel + "/eq/" + band + "/" + param)

        # Copy Compression Setting
        for param in ["thr", "ratio", "knee", "mgain", "attack", "hold", "release", "mix"]:
            await transferSetting(fohClient, iemClient, server, channel + "/dyn/" + param)

async def transferSetting(fohClient, iemClient, server, command):
    await fohClient.send_message(command, None)
    server.handle_request()
    await iemClient.send_message(command, server.lastVal)

if __name__ == "__main__":
    asyncio.run(main(SimpleClient(FOH_IP_ADDRESS), SimpleClient(IEM_IP_ADDRESS)))