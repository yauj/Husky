from pythonosc.dispatcher import Dispatcher
from pythonosc.osc_server import BlockingOSCUDPServer
from pythonosc.udp_client import SimpleUDPClient

def print_handler(address, *args):
    print(f"{address}: {args}")

dispatcher = Dispatcher()
dispatcher.set_default_handler("*", print_handler)
dispatcher.set_default_handler(print_handler)


client = SimpleUDPClient("10.246.1.15",10023)
server = BlockingOSCUDPServer(("0.0.0.0", 10023), dispatcher)
client._sock = server.socket

client.send_message("/info", "")
server.handle_request()