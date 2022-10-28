from time import sleep
from threading import Thread

from pyLib.cmdLine import cmdLine

class _clock():
    _instance = None
    clockPeriod = 1
    runClock = True
    
    def startClock(self):
        while self.runClock:
            cmdLine().printSuccess("Test")
            sleep(self.clockPeriod)
            
    def start(self):
        Thread(target= self.startClock).start()
        
    def stop(self):
        self.runClock = False

def clock():
    if _clock._instance is None:
        _clock._instance = _clock()
    return _clock._instance