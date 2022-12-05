import socket
import sys
sys.path.insert(0, '../')

import asyncio
import mido
from pythonosc.udp_client import SimpleUDPClient
from pythonosc.dispatcher import Dispatcher
from pythonosc.osc_server import BlockingOSCUDPServer
import threading
from time import time

MIDI_SERVER_NAME = "X32Helper"

# Simple Client that has async logic, since testing client has async logic
class SimpleClient(SimpleUDPClient):
    def __init__(self, name, ipAddress, test = False):
        super().__init__(ipAddress, 10023)
        self.name = name
        self.ipAddress = ipAddress
        self.test = test
        self.connected = False

    def connect(self, server):
        try:
            self.connected = True # Need this to send message
            self._sock = server.socket
            if self.ipAddress == "0.0.0.0":
                asyncio.run(self.send_message("/info", server.port))
            else:
                asyncio.run(self.send_message("/info", None))
            self.connected = server.handle_request_with_timeout()
        except Exception as ex:
            print(ex)
            self.connected = False

        if not self.test:
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
    def __init__(self, port = 10020):
        self.port = port
        self.retry = True
        self.lastVal = None

        dispatcher = Dispatcher()
        dispatcher.map("/info", self.printHandler)
        dispatcher.map("/xinfo", self.retryHandler)
        dispatcher.set_default_handler(self.singleArgHandler)

        super().__init__(("0.0.0.0", port), dispatcher)
        
        self.timeout = 0.1 # Timeout calls after 0.1 seconds
    
    def printHandler(self, address, *args):
        print(f"{address}: {args}")
        self.retry = False

    def singleArgHandler(self, address, *args):
        self.lastVal = args[0]
        self.retry = False

    def retryHandler(self, address, *args):
        self.retry = True

    # Throws Exception if timed out
    def handle_request(self):
        startTime = time()
        self.retry = True
        while (self.retry and time() - startTime < self.timeout):
            super().handle_request()

        if self.retry:
            raise TimeoutError("Timed out waiting for response. Please check if command is valid.")
    
    # Returns whether or not command was successful
    def handle_request_with_timeout(self):
        startTime = time()
        self.retry = True
        while (self.retry and time() - startTime < self.timeout):
            super().handle_request()

        return not self.retry

class AvailableIPs:
    def __init__(self):
        self.numThreads = 20

    def get(self):
        self.validIPs = []
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.settimeout(0.1)
            s.connect(("8.8.8.8", 80))
            self.thisIp = s.getsockname()[0]

            components = self.thisIp.split(".")
            self.prefix = components[0] + "." + components[1] + "." + components[2] + "."

            threads = []
            for index in range(0, self.numThreads):
                thread = threading.Thread(target = self.child, args = (index,))
                thread.start()
                threads.append(thread)

            for thread in threads:
                thread.join()
            
            return self.validIPs

    
    def child(self, index):
        server = RetryingServer(10000 + index)

        while index <= 255:
            ip = self.prefix + str(index)
            if ip == self.thisIp:
                ip = "0.0.0.0"
            client = SimpleClient("Test", ip, True)
            client.connect(server)
            if client.connected:
                self.validIPs.append(ip)

            index = index + self.numThreads

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
        return set(super().get_output_names())

# MIDI Server
class MIDIServer(mido.Backend):
    def __init__(self, port):
        super().__init__("mido.backends.rtmidi")
        self.input = None
        self.port = port
        self.callbackFunctions = []

    def open_input(self):
        if self.input is not None:
            self.input.close()
            print("Stopped listening to MIDI Port " + self.port.currentText())

        try:
            self.input = super().open_input(self.port.currentText())
            self.input.callback = self.callbackFunction
            print("Listening to MIDI Port " + self.port.currentText())
        except Exception as ex:
            print(ex)
            print("Failed to connect to MIDI at " + self.port.currentText())
            self.input = None

        return self.input is not None
    
    def callback(self, function):
        self.callbackFunctions.append(function)

    def callbackFunction(self, message):
        for function in self.callbackFunctions:
            function(message)

    def get_input_names(self):
        return set(super().get_input_names())

# MIDI Virtual Port
class MIDIVirtualPort(mido.Backend):
    def __init__(self):
        super().__init__("mido.backends.rtmidi")
        self.ioPort = super().open_ioport(MIDI_SERVER_NAME, True)
        self.ioPort.input.callback = self.ioPort.output.send
        print("Created MIDI IO Port " + MIDI_SERVER_NAME)