from itertools import islice
import logging
from math import ceil
import mido
import mido.backends.rtmidi # For PyInstaller
from pythonosc.udp_client import SimpleUDPClient
from pythonosc.dispatcher import Dispatcher
from pythonosc.osc_server import BlockingOSCUDPServer, ThreadingOSCUDPServer
import socket
import threading
from time import time, sleep
from util.constants import APP_NAME, NUM_THREADS, PORT, START_PORT
from uuid import uuid4

logger = logging.getLogger(__name__)

# Simple Client that has logic, since testing client has logic
class SimpleClient(SimpleUDPClient):
    def __init__(self, name, ipAddress, parent = True):
        super().__init__(ipAddress, PORT)
        self.name = name
        self.ipAddress = ipAddress
        self.parent = parent
        self.connected = False
        self.prevSettings = None # Previous settings before last bulk send command was fired.

    # Only parent needs to connect
    def connect(self, server):
        try:
            self.connected = True # Need this to send message
            self._sock = server.socket
            self.send_message("/info", None)
            self.connected = server.handle_request_with_timeout()
        except Exception as ex:
            logger.warning(ex)
            self.connected = False

        if self.parent:
            if self.connected:
                logger.info("Connected to " + self.name.upper() + " at " + self.ipAddress)
            else:
                logger.warning("Failed to connect to " + self.name.upper() + " at " + self.ipAddress)
        
        if server.subscription is not None:
            if self.connected:
                server.subscription.initIpAddress(self.ipAddress)
            else:
                server.subscription.initIpAddress(None)

        return self.connected

    def send_message(self, address, value):
        if self.connected or not self.parent:
            super().send_message(address, value)
        else:
            raise SystemError("Not Connected to " + self.name.upper() + " Client")
    
    # Undo previously applied settings
    # Returns whether or not settings were succesfully undone.
    def undo(self, dlg = None):
        if self.prevSettings is None:
            return False
        else:
            self.bulk_send_messages(self.prevSettings, dlg)
            self.prevSettings = None
            return True
    
    # Send a bunch of messages. Return results if arg is None.
    def bulk_send_messages(self, addresses, progressDialog = None, fadeAddresses = {}):
        if self.connected:
            # Get Current Commands
            curSettings = {}
            for address in addresses:
                if addresses[address] is not None:
                    curSettings[address] = None
            for address in fadeAddresses:
                curSettings[address] = None
            if (len(curSettings) == 0):
                self.prevSettings = None
            else:
                self.prevSettings = {}
                itr = iter(curSettings)
                size = ceil(len(curSettings) / NUM_THREADS)
                threads = []
                for index in range(0, NUM_THREADS):
                    slice = {}
                    for address in islice(itr, size):
                        slice[address] = curSettings[address]

                    th = threading.Thread(target = self.child, args = (index, slice, self.prevSettings))
                    th.start()
                    threads.append(th)
                for th in threads:
                    th.join()

            # Fire Commands
            results = {}
            itr = iter(addresses)
            size = ceil(len(addresses) / NUM_THREADS)
            threads = []
            for index in range(0, NUM_THREADS):
                slice = {}
                for address in islice(itr, size):
                    slice[address] = addresses[address]

                th = threading.Thread(target = self.child, args = (index, slice, results, progressDialog))
                th.start()
                threads.append(th)
            if len(fadeAddresses) > 0:
                th = threading.Thread(target = self.fadeChild, args = (fadeAddresses, progressDialog))
                th.start()
                threads.append(th)
            for th in threads:
                th.join()

            return results
        else:
            raise SystemError("Not Connected to " + self.name.upper() + " Client")
    
    def child(self, index, addresses, results, progressDialog = None):
        with RetryingServer(START_PORT + 1 + index) as server:
            client = SimpleClient(self.name, self.ipAddress, False)
            client._sock = server.socket
            for address in addresses:
                client.send_message(address, addresses[address])
                if addresses[address] is None:
                    try:
                        server.handle_request()
                    except TimeoutError:
                        logger.debug("Timed out listening to response to " + address + ". Retrying Once.")
                        client.send_message(address, addresses[address])
                        try:
                            server.handle_request()
                        except TimeoutError:
                            raise TimeoutError("Timed out listening to response to " + address)
                        
                        server.flush()

                    results[address] = server.lastVal
                else:
                    sleep(0.1) # Max 100 commands per second to ensure that no requests are dropped
                if progressDialog:
                    progressDialog.progressOne.emit()
    
    def fadeChild(self, fadeAddresses, progressDialog = None):
        fadeAddresses = fadeAddresses.copy()
        for address in fadeAddresses:
            fadeAddresses[address]["endFired"] = 0 # Number of times end command was fired

        client = SimpleClient(self.name, self.ipAddress, False)
        startTime = time()
        while len(fadeAddresses) > 0:
            for address in fadeAddresses.copy():
                ratio = (time() - startTime) / fadeAddresses[address]["fadeTime"]
                if ratio >= 1:
                    client.send_message(address, fadeAddresses[address]["endVal"])
                    fadeAddresses[address]["endFired"] = fadeAddresses[address]["endFired"] + 1
                    if fadeAddresses[address]["endFired"] == 5: # Send End Command 5 times, to ensure that end state is reached
                        del fadeAddresses[address]
                        if progressDialog:
                            progressDialog.progressOne.emit()
                else:
                    client.send_message(
                        address,
                        round(self.prevSettings[address] + (ratio * (fadeAddresses[address]["endVal"] - self.prevSettings[address])), 5)
                    )
            sleep(0.01 * len(fadeAddresses)) # Max 100 commands per second to ensure that no requests are dropped

# Server which retries attempting to get if /xinfo message passed back 
class RetryingServer(BlockingOSCUDPServer):
    def __init__(self, port, mixerName = None):
        self.port = port
        self.retry = True
        self.lastVal = None

        dispatcher = Dispatcher()
        dispatcher.map("/info", self.printHandler)
        dispatcher.map("/xinfo", self.retryHandler)
        dispatcher.set_default_handler(self.singleArgHandler)

        super().__init__(("", port), dispatcher)
        
        self.timeout = 1 # Timeout calls after 1 second

        self.subscription = SubscriptionServer(mixerName, self.port + 1) if mixerName is not None else None

    def printHandler(self, address, *args):
        logger.debug(f"{address}: {args}")
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
    
    # Flush all incoming requests for the next second
    def flush(self):
        startTime = time()
        self.retry = True
        while (time() - startTime < self.timeout):
            super().handle_request()

    def shutdown(self):
        if self.subscription is not None:
            self.subscription.shutdown()
    
    # Returns whether or not command was successful
    def handle_request_with_timeout(self):
        startTime = time()
        self.retry = True
        while (self.retry and time() - startTime < self.timeout):
            super().handle_request()

        return not self.retry

# OSC Subscription
class SubscriptionServer(ThreadingOSCUDPServer):
    def __init__(self, mixerName, port):
        dispatcher = Dispatcher()
        dispatcher.set_default_handler(self.functionHandler)

        super().__init__(("", port), dispatcher)

        self.mixerName = mixerName
        self.ipAddress = None
        self.subscriptions = {}
        self.activeSubscriptions = {} # Internal
        self.shutdownFlag = False
        threading.Thread(target = self.serve_forever).start()
        threading.Thread(target = self.renewThread).start()

    def initIpAddress(self, ipAddress):
        self.activeSubscriptions = {} # Kill all current renewals
        self.ipAddress = ipAddress
        if self.ipAddress is not None:
            threading.Thread(target = self.subscribeThread).start()
    
    def shutdown(self):
        self.shutdownFlag = True # Finishes up renew thread
        super().shutdown() # Finishes up server thread

    def functionHandler(self, address, *args):
        if address in self.subscriptions:
            self.subscriptions[address]["command"](self.mixerName, address, args[0])

    def add(self, address, command, alias = None, param1 = 0, param2 = 0, paramTimeFactor = 1):
        record = {
            "address": address,
            "command": command
        }

        if "/meters/" in address:
            if alias is not None:
                record["subCmd"] = "/batchsubscribe"
                record["alias"] = alias
                record["param1"] = param1
                record["param2"] = param2
                record["paramTimeFactor"] = paramTimeFactor
            else:
                record["subCmd"] = "/meters"
        else:
            if alias is not None:
                record["subCmd"] = "/formatsubscribe"
                record["alias"] = alias
                record["param1"] = param1
                record["param2"] = param2
                record["paramTimeFactor"] = paramTimeFactor
            else:
                record["subCmd"] = "/subscribe"

        if alias is not None:
            self.subscriptions[alias] = record
        else:
            self.subscriptions[address] = record

        if self.ipAddress is not None:
            client = SimpleUDPClient(self.ipAddress, PORT)
            client._sock = self.socket

            if "alias" in record:
                client.send_message(record["subCmd"], [record["alias"], record["address"], record["param1"], record["param2"], record["paramTimeFactor"]])
                self.activeSubscriptions[alias] = record
            else:
                client.send_message(record["subCmd"], record["address"])
                self.activeSubscriptions[address] = record
    
    def remove(self, address):
        self.activeSubscriptions.pop(address, None)
        self.subscriptions.pop(address, None)
        # self.client.send_message("/unsubscribe", address) Just allow subscription to expire
    
    def subscribeThread(self):
        self.sendCommands("/subscribe", self.subscriptions)
        self.activeSubscriptions = self.subscriptions.copy()

    def renewThread(self):
        while not self.shutdownFlag:
            self.sendCommands("/renew", self.activeSubscriptions)
    
    def sendCommands(self, command, args):
        args = args.copy()
        startTime = time()
        if self.ipAddress is not None and len(args) > 0:
            client = SimpleUDPClient(self.ipAddress, PORT)
            client._sock = self.socket
            sleepTime = 4.0 / len(args) # Spread out commands across approx 4.0 seconds
            for address in args:
                itrTime = time()
            
                if self.shutdownFlag or len(self.activeSubscriptions) == 0:
                    return # Exit early if shutdown or reconnection going on

                if command == "/renew":
                    if "alias" in args[address]:
                        client.send_message(command, args[address]["alias"])
                    else:
                        client.send_message(command, address)
                else:
                    if "alias" in args[address]:
                        client.send_message(args[address]["subCmd"], [args[address]["alias"], args[address]["address"], args[address]["param1"], args[address]["param2"], args[address]["paramTimeFactor"]])
                    else:
                        client.send_message(args[address]["subCmd"], args[address]["address"])

                # If time to run is over sleep time, want to just skip sleep
                # If over 4.0 seconds already, just want to spew the rest out.
                while time() - startTime < 4.0 and time() - itrTime < sleepTime:
                    if self.shutdownFlag or len(self.activeSubscriptions) == 0:
                        return # Exit early if shutdown or reconnection going on
                    sleep(max(min(sleepTime - (time() - itrTime), 0.1), 0))

        while time() - startTime < 4.0: # If still under 4.0 seconds, then we want to wait the rest out.
            if self.shutdownFlag:
                return # Exit early if shutdown
            sleep(0.1)

class AvailableIPs:
    def get(self):
        self.validIPs = []
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.settimeout(0.1)
            try:
                s.connect(("8.8.8.8", 80))
                self.thisIp = s.getsockname()[0]
                components = self.thisIp.split(".")
                self.prefix = components[0] + "." + components[1] + "." + components[2] + "."

                threads = []
                for index in range(0, NUM_THREADS):
                    th = threading.Thread(target = self.child, args = (index,))
                    th.start()
                    threads.append(th)

                for th in threads:
                    th.join()
                
                return self.validIPs
            except OSError as ex:
                if str(ex) == "[Errno 51] Network is unreachable":
                    logger.debug("Not Connected to Internet. Just checking localhost")
                    with RetryingServer(START_PORT + 1) as server:
                        server.timeout = 0.1
                        ip = ""
                        client = SimpleClient("Test", ip, False)
                        if client.connect(server):
                            return [ip]
                        else:
                            return []
                else:
                    raise ex
    
    def child(self, index):
        with RetryingServer(START_PORT + 1 + index) as server:
            server.timeout = 0.1
            for i in range(index, 256, NUM_THREADS):
                ip = self.prefix + str(i)
                if ip == self.thisIp:
                    ip = ""
                client = SimpleClient("Test", ip, False)
                if client.connect(server):
                    self.validIPs.append(ip)

# Atem Client - Creates a single threaded connection to a local AtemOSC application
class AtemClient(SimpleUDPClient):
    def __init__(self, port):
        super().__init__("", port)
        self.prevSettings = None # Previous settings before last bulk send command was fired.
    
    # Undo previously applied settings
    # Returns whether or not settings were succesfully undone.
    def undo(self, dlg = None):
        if self.prevSettings is None:
            return False
        else:
            self.bulk_send_messages(self.prevSettings, dlg)
            self.prevSettings = None
            return True
    
    # Send a bunch of messages. Return results if arg is None.
    def bulk_send_messages(self, addresses, progressDialog = None, fadeAddresses = {}):
        # Send Addresses
        for address in addresses:
            self.send_message(address, addresses[address])
            if progressDialog:
                progressDialog.progressOne.emit()
        
        # Send Fader
        for address in fadeAddresses:
            fadeAddresses[address]["endFired"] = 0 # Number of times end command was fired
        startTime = time()
        while len(fadeAddresses) > 0:
            for address in fadeAddresses.copy():
                ratio = (time() - startTime) / fadeAddresses[address]["fadeTime"]
                if ratio >= 1:
                    self.send_message(address, fadeAddresses[address]["endVal"])
                    fadeAddresses[address]["endFired"] = fadeAddresses[address]["endFired"] + 1
                    if fadeAddresses[address]["endFired"] == 5: # Send End Command 5 times, to ensure that end state is reached
                        del fadeAddresses[address]
                        if progressDialog:
                            progressDialog.progressOne.emit()
                else:
                    self.send_message(
                        address,
                        round(self.prevSettings[address] + (ratio * (fadeAddresses[address]["endVal"] - self.prevSettings[address])), 5)
                    )
            sleep(0.01 * len(fadeAddresses)) # Max 100 commands per second to ensure that no requests are dropped

# Atem Subscription
class AtemSubscriptionServer: # Wrapper for Atem Server
    def __init__(self):
        self.subscription = AtemServer()
    def shutdown(self):
        self.subscription.shutdown()
class AtemServer(ThreadingOSCUDPServer):
    def __init__(self):
        dispatcher = Dispatcher()
        dispatcher.set_default_handler(self.functionHandler)

        super().__init__(("", START_PORT), dispatcher)

        self.subscriptions = {}
        threading.Thread(target = self.serve_forever).start()
    
    def shutdown(self):
        super().shutdown() # Finishes up server thread

    def functionHandler(self, address, *args):
        if address in self.subscriptions:
            self.subscriptions[address]("atem", address, args[0])

    def add(self, address, command):
        self.subscriptions[address] = command
    
    def remove(self, address):
        self.subscriptions.pop(address, None)

# MIDI Client
class MIDIClient(mido.Backend):
    def __init__(self, port):
        super().__init__("mido.backends.rtmidi")
        self.port = port
        self.output = None
    
    def open_output(self):
        try:
            self.output = super().open_output(self.port)
            logger.info("Connected to MIDI at " + self.port)
        except Exception as ex:
            logger.warning(ex)
            logger.warning("Failed to connect to MIDI at " + self.port)
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
    def __init__(self, port = None, widgets = None):
        super().__init__("mido.backends.rtmidi")
        self.ioPort = None
        self.port = port
        self.widgets = widgets # This goes against philosophy to make servers lightweight
        self.subscriptions = {}

    def open_ioPort(self):
        self.close()

        try:
            self.ioPort = super().open_ioport(self.port)
            self.ioPort.input.callback = self.callbackFunction
            logger.info("Listening to MIDI Port " + self.port)
        except Exception as ex:
            logger.warning(ex)
            logger.warning("Failed to listen to MIDI at " + self.port)
            self.ioPort = None

        return self.ioPort is not None
    
    def addCallback(self, params):
        id = str(uuid4())
        self.subscriptions[id] = params
        return id

    def editCallback(self, id, params):
        self.subscriptions[id] = params
    
    def removeCallback(self, id):
        del self.subscriptions[id]
    
    def getCallback(self, id):
        return self.subscriptions[id]

    def getCallbacks(self):
        return self.subscriptions

    def callbackFunction(self, message):
        for id in self.subscriptions:
            if message.type == "control_change" and self.subscriptions[id]["midi"]["type"] == "Control Change":
                if message.channel + 1 == self.subscriptions[id]["midi"]["channel"] and message.control == self.subscriptions[id]["midi"]["control"]:
                    if self.subscriptions[id]["command"]["type"] == "Cue":
                        if message.value > 0:
                            self.processCue(id)
                    elif self.subscriptions[id]["command"]["type"] == "Fader":
                        self.processFader(id, message)
            elif message.type == "note_on" and self.subscriptions[id]["midi"]["type"] == "Note":
                # Only support cues
                if message.channel + 1 == self.subscriptions[id]["midi"]["channel"] \
                    and message.note == self.subscriptions[id]["midi"]["control"] \
                    and self.subscriptions[id]["command"]["type"] == "Cue":
                        self.processCue(id)
    
    def processCue(self, id):
        page = self.getPageIdx(self.widgets["tabs"]["Cue"], self.subscriptions[id]["command"]["page"])
        if self.subscriptions[id]["command"]["index"] == "Prev Page":
            if page > 0:
                self.widgets["tabs"]["Cue"].setCurrentIndex(page - 1)
        elif self.subscriptions[id]["command"]["index"] == "Next Page":
            if page < self.widgets["tabs"]["Cue"].count() - 1:
                self.widgets["tabs"]["Cue"].setCurrentIndex(page + 1)
        else:
            idx = int(self.subscriptions[id]["command"]["index"]) - 1
            if idx < len(self.widgets["tabs"]["Cue"].widget(page).buttons):
                self.widgets["tabs"]["Cue"].widget(page).buttons[idx].clicked()
    
    def processFader(self, id, message):
        page = self.getPageIdx(self.widgets["tabs"]["Fader"], self.subscriptions[id]["command"]["page"])
        if self.subscriptions[id]["command"]["index"] == "Prev Page":
            if message.value > 0 and page > 0:
                self.widgets["tabs"]["Fader"].setCurrentIndex(page - 1)
        elif self.subscriptions[id]["command"]["index"] == "Next Page":
            if message.value > 0 and page < self.widgets["tabs"]["Fader"].count() - 1:
                self.widgets["tabs"]["Fader"].setCurrentIndex(page + 1)
        else:
            idx = int(self.subscriptions[id]["command"]["index"]) - 1
            if idx < len(self.widgets["tabs"]["Fader"].widget(page).faders):
                fader = self.widgets["tabs"]["Fader"].widget(page).faders[idx]
                if fader.lock.acquire("midi " + id + " " + self.port):
                    fader.setValue(message.value)

    # Only support feedback for fader
    def processFeedback(self, page, index, value, ogId = None):
        if self.ioPort is not None:
            for id in self.subscriptions:
                if ogId != id \
                    and self.subscriptions[id]["command"]["type"] == "Fader" \
                    and self.subscriptions[id]["command"]["index"] == index:
                        if self.subscriptions[id]["command"]["page"] == page \
                            or (self.subscriptions[id]["command"]["page"] == "CURRENT" and self.widgets["tabs"]["Fader"].currentIndex() == page):
                            channel = self.subscriptions[id]["midi"]["channel"] - 1
                            control = self.subscriptions[id]["midi"]["control"]
                            if self.subscriptions[id]["midi"]["type"] == "Control Change":
                                type = "control_change"
                                self.ioPort.output.send(mido.Message(type = type, channel = channel, control = control, value = value))
                            elif self.subscriptions[id]["midi"]["type"] == "Note":
                                type = "note_off" if value == 0 else "note_on"
                                self.ioPort.output.send(mido.Message(type = type, channel = channel, note = control))

    def getPageIdx(self, tabs, value):
        if value == "CURRENT":
            return tabs.currentIndex()
        else:
            for idx in range(0, tabs.count()):
                if value == tabs.tabText(idx):
                    return idx
        return None
    
    def connected(self):
        return self.ioPort is not None
    
    def close(self):
        if self.ioPort is not None:
            self.ioPort.close()
            logger.info("Stopped listening to MIDI Port " + self.port)
            self.ioPort = None

    def get_ioport_names(self):
        return set(super().get_ioport_names())

# MIDI Virtual Port
class MIDIVirtualPort(mido.Backend):
    def __init__(self):
        super().__init__("mido.backends.rtmidi")
        self.ioPort = super().open_ioport(APP_NAME, True)
        self.ioPort.input.callback = self.ioPort.output.send
        logger.info("Created MIDI IO Port " + APP_NAME)