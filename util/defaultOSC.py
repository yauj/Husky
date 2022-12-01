import sys

import mido
sys.path.insert(0, '../')

import asyncio
from pythonosc.udp_client import SimpleUDPClient
from pythonosc.dispatcher import Dispatcher
from pythonosc.osc_server import BlockingOSCUDPServer
from time import time

MIDI_SERVER_NAME = "X32Helper"

# Simple Client that has async logic, since testing client has async logic
class SimpleClient(SimpleUDPClient):
    def __init__(self, name, ipAddress):
        super().__init__(ipAddress, 10023)
        self.name = name
        self.ipAddress = ipAddress
        self.connected = False

    def connect(self, server):
        try:
            self.connected = True # Need this to send message
            self._sock = server.socket
            asyncio.run(self.send_message("/info", None))
            self.connected = server.handle_request_with_timeout()
        except Exception as ex:
            print(ex)
            self.connected = False

        if self.connected:
            print("Connected to " + self.name.upper() + " at " + self.ipAddress)
        else:
            print("Failed to connect to " + self.name.upper() + " at " + self.ipAddress)

        return self.connected

    async def send_message(self, address, value):
        if self.connected:
            super().send_message(address, value)
        else:
            raise SystemError("Not Connected to " + self.name.upper() + " Client")

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
        self.timeout = None
        self._retry = True
        while (self._retry):
            super().handle_request()
    
    # Timeout after 1 seconds. Returns if call succeeded.
    def handle_request_with_timeout(self):
        self.timeout = 1
        startTime = time()
        self._retry = True
        while (self._retry and time() - startTime < 1.0):
            super().handle_request()

        return not self._retry

# MIDI Client
class MIDIClient(mido.Backend):
    def __init__(self, port):
        super().__init__("mido.backends.rtmidi")
        self.port = port
        self.output = None
    
    def open_output(self):
        try:
            self.output = super().open_output(self.port)
            print("Connected to MIDI at " + self.port)
        except Exception as ex:
            print(ex)
            print("Failed to connect to MIDI at " + self.port)
            self.output = None

        return self.output is not None
    
    def send(self, message):
        if self.output is not None:
            self.output.send(message)
        else:
            raise SystemError("Not Connected to MIDI Port")
    
    def get_output_names(self):
        names = set(super().get_output_names())
        if MIDI_SERVER_NAME in names:
            names.remove(MIDI_SERVER_NAME)
        return names

# MIDI Server
class MIDIServer(mido.Backend):
    def __init__(self):
        super().__init__("mido.backends.rtmidi")
        self.input = super().open_input(MIDI_SERVER_NAME, True)
        print("Created MIDI reciever " + MIDI_SERVER_NAME)
    
    def callback(self, function):
        self.input.callback = function