import asyncio
from pythonosc.dispatcher import Dispatcher
from pythonosc.osc_server import BlockingOSCUDPServer
from pythonosc.udp_client import SimpleUDPClient

async def serverEmulator():
    dispatcher = Dispatcher()
    dispatcher.set_default_handler(loopbackHandler)

    server = BlockingOSCUDPServer(("0.0.0.0", 10023), dispatcher)

    while True:
        server.handle_request()
    
def loopbackHandler(address, *args):
    if args:
        print(f"{address}: {args}")
    else:
        client = SimpleUDPClient("0.0.0.0", 10024)
        client.send_message("/xinfo", None) # Simulate metadata calls
        client.send_message(address, 0.0)

asyncio.run(serverEmulator())