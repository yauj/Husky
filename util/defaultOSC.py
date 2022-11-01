import sys
sys.path.insert(0, '../')

from pythonosc.udp_client import SimpleUDPClient
from pythonosc.dispatcher import Dispatcher
from pythonosc.osc_server import BlockingOSCUDPServer

# Simple Client that has async logic, since testing client has async logic
class SimpleClient(SimpleUDPClient):
    def __init__(self, ipAddress):
        super().__init__(ipAddress, 10023)

    async def send_message(self, address, value):
        super().send_message(address, value)

# Server which retries attempting to get if /xinfo message passed back 
class RetryingServer(BlockingOSCUDPServer):
    @property
    def lastVal(self):
        return self._lastVal # Previous args[0]

    def __init__(self):
        self._retry = True
        self._lastVal = None

        def printHandler(address, *args):
            print(f"{address}: {args}")
            self._retry = False

        def singleArgHandler(address, *args):
            self._lastVal = args[0]
            self._retry = False

        def retryHandler(address, *args):
            self._retry = True
        
        dispatcher = Dispatcher()
        dispatcher.map("/info", printHandler)
        dispatcher.map("/xinfo", retryHandler)
        dispatcher.set_default_handler(singleArgHandler)

        super().__init__(("0.0.0.0", 10024), dispatcher)

    def handle_request(self):
        self._retry = True
        while (self._retry):
            super().handle_request()
