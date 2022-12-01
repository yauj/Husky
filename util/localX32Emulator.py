from pythonosc.dispatcher import Dispatcher
from pythonosc.osc_server import BlockingOSCUDPServer
from pythonosc.udp_client import SimpleUDPClient

class X32Emulator():
    def __init__(self):
        self.client = SimpleUDPClient("0.0.0.0", 10024)
        dispatcher = Dispatcher()
        dispatcher.set_default_handler(self.loopbackHandler)
        self.server = BlockingOSCUDPServer(("0.0.0.0", 10023), dispatcher)
        print("Server Started for port " + str(self.server.server_address))

    def start(self):
        try:
            while True:
                self.server.handle_request()
        finally:
            print("Closed Server")
        
    def loopbackHandler(self, address, *args):
        if args:
            print(f"{address}: {args}")
        else:
            self.client.send_message("/xinfo", None) # Simulate metadata calls
            self.client.send_message(address, 0.0)

X32Emulator().start()