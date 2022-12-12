import threading
from time import time

class OwnerLock():
    def __init__(self):
        self.lock = threading.Lock()
        self.owner = ""
        self.timer = None

    # Returns True if lock acquired
    def acquire(self, newOwner):
        with self.lock:
            if newOwner == "master":
                # Always override current lock for master
                self.owner = "master"
                self.timer = None
                return True
            elif self.owner == "":
                # No Current Owner
                self.owner = newOwner
                self.timer = time()
                return True
            elif newOwner == self.owner:
                # Same Owner
                self.timer = time()
                return True
            elif self.owner == "master":
                # Unable to override master lock
                return False
            elif time() - self.timer < 0.5:
                # Lock hasn't expired
                return False
            else:
                self.owner = newOwner
                self.timer = time()
                return True
    
    def acquireMaster(self):
        return self.acquire("master")

    def release(self):
        with self.lock:
            self.owner = ""
            self.timer = None