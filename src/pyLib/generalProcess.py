# possibleStates = ["Pronto", "Entrada", "Bloqueado"]

class process():
    def __init__(self, processName: str, baseState: str, baseAddress: int):
        self.name = processName
        self.state = baseState
        self.programCounter = baseAddress
        self.accumulator = 0
        self.halted = (processName == "Espera")
        self.flagI = 0
        self.flagN = 0
        self.flagZ = 0
        return
    
    def getStatus(self) -> list[int, int, bool, int, int, int]:
        return [self.programCounter, self.accumulator, self.halted, self.flagI, self.flagN, self.flagZ]
    
    def setStatus(self, status: list[int, int, bool, int, int, int]):
        self.programCounter = status[0]
        self.accumulator = status[1]
        self.halted = status[2]
        self.flagI = status[3]
        self.flagN = status[4]
        self.flagZ = status[5]
        return