from time import sleep
from threading import Thread

from pyLib.configs import *

import pyLib.interface
import pyLib.processAdmin

class _clock():
    _instance = None
    runClock = True
    
    def startClock(self):
        while self.runClock:
            pyLib.processAdmin.processAdmin().clockRise()
            pyLib.interface.interface().refresh()
            sleep(1/clocksPerSecond)
            
    def start(self):
        Thread(target= self.startClock).start()
        
    def stop(self):
        self.runClock = False

def clock():
    if _clock._instance is None:
        _clock._instance = _clock()
    return _clock._instance