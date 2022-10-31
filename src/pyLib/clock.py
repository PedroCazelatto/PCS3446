from time import sleep
from threading import Thread

import pyLib.interface
import pyLib.processAdmin

class _clock():
    _instance = None
    clockPeriod = 1
    runClock = True
    
    def startClock(self):
        while self.runClock:
            pyLib.processAdmin.processAdmin().clockRise()
            pyLib.interface.interface().refresh()
            sleep(self.clockPeriod)
            
    def start(self):
        Thread(target= self.startClock).start()
        
    def stop(self):
        self.runClock = False

def clock():
    if _clock._instance is None:
        _clock._instance = _clock()
    return _clock._instance