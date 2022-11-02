# possibleStates = ["Executando", "Pronto", "Entrada", "Bloqueado"]

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