from pythonosc.dispatcher import Dispatcher
from pythonosc.osc_server import ThreadingOSCUDPServer
from pythonosc.udp_client import SimpleUDPClient
from defaultOSC import NUM_THREADS

class X32Emulator():
    def __init__(self):
        self.client = SimpleUDPClient("0.0.0.0", 10000 + NUM_THREADS)
        dispatcher = Dispatcher()
        dispatcher.set_default_handler(self.loopbackHandler)
        self.server = ThreadingOSCUDPServer(("0.0.0.0", 10023), dispatcher)
        print("Server Started for port " + str(self.server.server_address))

    def start(self):
        try:
            self.server.serve_forever()
        finally:
            print("Closed Server")
        
    def loopbackHandler(self, address, *args):
        if address == "/info":
            if args:
                client = SimpleUDPClient("0.0.0.0", args[0])
                client.send_message("/info", ('V0.00', 'osc-server', 'LOCAL', '0.00-0'))
            else:
                self.client.send_message("/info", ('V0.00', 'osc-server', 'LOCAL', '0.00-0'))
        elif args:
            print(f"{address}: {args}")
        else:
            self.client.send_message("/xinfo", None) # Simulate metadata calls
            self.client.send_message(address, 0.0)

X32Emulator().start()