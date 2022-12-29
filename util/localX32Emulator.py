from pythonosc.dispatcher import Dispatcher
from pythonosc.osc_server import ThreadingOSCUDPServer
from pythonosc.udp_client import SimpleUDPClient
import sys

DEBUG = False

class X32Emulator():
    def __init__(self, port):
        dispatcher = Dispatcher()
        dispatcher.set_default_handler(self.loopbackHandler, True)
        self.server = ThreadingOSCUDPServer(("0.0.0.0", port), dispatcher)
        print("Server Started for port " + str(self.server.server_address))

        try:
            self.server.serve_forever()
        finally:
            print("Closed Server")
        
    def loopbackHandler(self, clientIP, address, *args):
        client = SimpleUDPClient(clientIP[0], clientIP[1])
        if address == "/info":
            client.send_message("/info", ('V0.00', 'osc-server', 'LOCAL', '0.00-0'))
        elif address == "/subscribe" or address == "/renew":
            client.send_message("/xinfo", None) # Simulate metadata calls
            client.send_message(args[0], 0.0)
            if DEBUG: print(f"Sending {args[0]}: 0.0")
        elif args:
            print(f"{address}: {args}")
        else:
            client.send_message("/xinfo", None) # Simulate metadata calls
            client.send_message(address, 0.0)
            if DEBUG: print(f"Sending {address}: 0.0")

if len(sys.argv) > 1:
    X32Emulator(int(sys.argv[1]))
else:
    X32Emulator(10023)