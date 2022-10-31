import pyLib.cmdLine
import pyLib.memory
import pyLib.processAdmin

from pyLib.infoLists import operations

def toBin(integer: int) -> str:
    binary = bin(integer)[2:]
    leadZeros = '0' * (8 - len(binary))
    return leadZeros + binary

class _cpu():
    _instance = None
    
    programCounter = -1
    accumulator = 0
    halted = True
    
    flagI = 0
    flagN = 0
    flagZ = 0
    
    def getStatus(self):
        return [self.programCounter, self.accumulator, self.halted, self.flagI, self.flagN, self.flagZ]
    
    def setStatus(self, status: list):
        self.programCounter = status[0]
        self.accumulator = status[1]
        self.halted = status[2]
        self.flagI = status[3]
        self.flagN = status[4]
        self.flagZ = status[5]
        return
    
    def processInstruction(self):
        if self.halted or self.programCounter < 0:
            return
        instruction = pyLib.memory.memory().readMemory(self.programCounter)
        opcode = operations[int(instruction[:14], base= 2)]
        operand = int(instruction[14:], base= 2)
        pyLib.cmdLine.cmdLine().printExit(opcode + " " + instruction[14:])
        pyLib.cmdLine.cmdLine().refresh()
        if opcode == "HLT":
            self.halted = True
            pyLib.processAdmin.processAdmin().changeProcess()
        elif opcode == "LDA":
            self.accumulator = int(pyLib.memory.memory().readMemory(operand), base= 2)
        elif opcode == "STA":
            pyLib.memory.memory().writeMemory(operand, self.accumulator)
        elif opcode == "NEG":
            self.accumulator = - self.accumulator
        elif opcode == "ADD":
            self.accumulator += int(pyLib.memory.memory().readMemory(operand), base= 2)
        elif opcode == "SUB":
            self.accumulator -= int(pyLib.memory.memory().readMemory(operand), base= 2)
        elif opcode == "MUL":
            self.accumulator *= int(pyLib.memory.memory().readMemory(operand), base= 2)
        elif opcode == "DIV":
            self.accumulator //= int(pyLib.memory.memory().readMemory(operand), base= 2)
        elif opcode == "REM":
            self.accumulator %= int(pyLib.memory.memory().readMemory(operand), base= 2)
        elif opcode == "AND":
            self.accumulator &= int(pyLib.memory.memory().readMemory(operand), base= 2)
        elif opcode == "ORR":
            self.accumulator |= int(pyLib.memory.memory().readMemory(operand), base= 2)
        elif opcode == "NOT":
            self.accumulator = ~ self.accumulator
        elif opcode == "XOR":
            self.accumulator ^= int(pyLib.memory.memory().readMemory(operand), base= 2)
        elif opcode == "TXT":
            number = str(self.accumulator)
            textLen = len(number)
            word = toBin(textLen)
            for i in range(textLen):
                char = toBin(ord(number[i]))
                if i % 4 != 3:
                    word += char
                else:
                    value = int(word, base= 2)
                    pyLib.memory.memory().writeMemory(operand + i // 4, value)
                    word = ''
            if textLen % 4 != 3:
                word += (('0' * 8) * (3 - textLen % 4))
                value = int(word, base= 2)
                pyLib.memory.memory().writeMemory(operand + textLen // 4, value)
        elif opcode == "WRD":
            firstWord = pyLib.memory.memory().readMemory(operand)
            numberChars = int(firstWord[:8], base= 2)
            word = ''
            for i in range(numberChars // 4+1):
                word += pyLib.memory.memory().readMemory(operand + i)
            number = 0
            for i in range(numberChars):
                number = 10*number + int(chr(int(word[8*(i+1):8*(i+2)], base= 2)))
            self.accumulator = number
        elif opcode == "INP":
            pass
        elif opcode == "OUT":
            firstWord = pyLib.memory.memory().readMemory(operand)
            numberChars = int(firstWord[:8], base= 2)
            word = ''
            for i in range(numberChars // 4 +1):
                word += pyLib.memory.memory().readMemory(operand + i)
            toPrint = ''
            for i in range(numberChars):
                toPrint += chr(int(word[8*(i+1):8*(i+2)], base= 2))
            pyLib.cmdLine.cmdLine().printExit(toPrint)
        elif opcode == "CMP":
            if self.accumulator - int(pyLib.memory.memory().readMemory(operand), base= 2) == 0:
                self.flagZ = 1
            if self.accumulator - int(pyLib.memory.memory().readMemory(operand), base= 2) < 0:
                self.flagN = 1
        elif opcode == "BEQ":
            if self.flagZ == 1:
                self.programCounter = operand
        elif opcode == "BNE":
            if self.flagZ == 0:
                self.programCounter = operand
        elif opcode == "JMP":
            self.programCounter = operand
        elif opcode == "SET":
            bits = bin(operand)[-3:]
            self.flagI = bits[0]
            self.flagN = bits[1]
            self.flagZ = bits[2]
        self.programCounter += 1
        return

def cpu():
    if _cpu._instance is None:
        _cpu._instance = _cpu()
    return _cpu._instance