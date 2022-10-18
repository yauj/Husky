import asyncio
from pythonosc.dispatcher import Dispatcher
from pythonosc.osc_server import AsyncIOOSCUDPServer
from pythonosc.udp_client import SimpleUDPClient

runFlag = True

def execute(main):
    asyncio.run(coroutine(main))

async def coroutine(main):
    await asyncio.gather(serverEmulator(), mainTask(main))

async def mainTask(main):
    global runFlag
    await main(AsyncClient())
    runFlag = False

async def serverEmulator():
    dispatcher = Dispatcher()
    dispatcher.set_default_handler(loopbackHandler)

    server = AsyncIOOSCUDPServer(("0.0.0.0", 10023), dispatcher, asyncio.get_event_loop())

    transport = await server.create_serve_endpoint()

    await sleepLoop()

    transport.close()

async def sleepLoop():
    global runFlag
    while runFlag:
        await asyncio.sleep(0.0001) # Give thread back to main program

def loopbackHandler(address, *args):
    if args:
        print(f"{address}: {args}")
    else:
        client = SimpleUDPClient("0.0.0.0", 10024)
        client.send_message("/xinfo", None) # Simulate metadata calls
        client.send_message(address, 0.0)

class AsyncClient(SimpleUDPClient):
    def __init__(self):
        super().__init__("0.0.0.0", 10023)

    async def send_message(self, address, value):
        super().send_message(address, value)
        await asyncio.sleep(0.0001) # Allow Local Server to pickup request