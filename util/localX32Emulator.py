from pythonosc.dispatcher import Dispatcher
from pythonosc.osc_server import ThreadingOSCUDPServer
from pythonosc.udp_client import SimpleUDPClient

class X32Emulator():
    def __init__(self):
        dispatcher = Dispatcher()
        dispatcher.set_default_handler(self.loopbackHandler, True)
        self.server = ThreadingOSCUDPServer(("0.0.0.0", 10023), dispatcher)
        print("Server Started for port " + str(self.server.server_address))

    def start(self):
        try:
            self.server.serve_forever()
        finally:
            print("Closed Server")
        
    def loopbackHandler(self, clientIP, address, *args):
        client = SimpleUDPClient(clientIP[0], clientIP[1])
        if address == "/info":
            client.send_message("/info", ('V0.00', 'osc-server', 'LOCAL', '0.00-0'))
        elif args:
            print(f"{address}: {args}")
        else:
            client.send_message("/xinfo", None) # Simulate metadata calls
            client.send_message(address, 0.0)

X32Emulator().start()