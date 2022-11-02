import pyLib.cmdLine
import pyLib.memory
import pyLib.processAdmin
import pyLib.generalProcess

from pyLib.configs import *
from pyLib.usefulFuncs import *

from pyLib.infoLists import operations

class _cpu():
    _instance = None
    
    actualProcess = pyLib.generalProcess.process("Espera", "Bloqueado", -1)
    
    def getProcess(self):
        return self.actualProcess
    
    def setProcess(self, process: pyLib.generalProcess.process):
        self.actualProcess = process
        return
    
    def processInstruction(self):
        if self.actualProcess.halted or self.actualProcess.programCounter < 0:
            return
        instruction = pyLib.memory.memory().readMemory(self.actualProcess.programCounter)
        opcode = operations[int(instruction[:5], base= 2)]
        operand = int(instruction[5:], base= 2)
        if opcode == "HLT":
            self.actualProcess.halted = True
            pyLib.cmdLine.cmdLine().printSuccess(self.actualProcess.name + " terminou de executar")
            pyLib.processAdmin.processAdmin().stopCurrentProcess()
            return
        elif opcode == "LDA":
            if self.actualProcess.flagI == 0:
                self.actualProcess.accumulator = int(pyLib.memory.memory().readMemory(operand), base= 2)
            else:
                address = int(pyLib.memory.memory().readMemory(operand), base= 2)
                self.actualProcess.accumulator = int(pyLib.memory.memory().readMemory(address), base= 2)
        elif opcode == "STA":
            if self.actualProcess.flagI == 0:
                pyLib.memory.memory().writeMemory(operand, self.actualProcess.accumulator)
            else:
                address = int(pyLib.memory.memory().readMemory(operand), base= 2)
                pyLib.memory.memory().writeMemory(address, self.actualProcess.accumulator)
        elif opcode == "NEG":
            self.actualProcess.accumulator = - self.actualProcess.accumulator
        elif opcode == "ADD":
            self.actualProcess.accumulator += int(pyLib.memory.memory().readMemory(operand), base= 2)
        elif opcode == "SUB":
            self.actualProcess.accumulator -= int(pyLib.memory.memory().readMemory(operand), base= 2)
        elif opcode == "MUL":
            self.actualProcess.accumulator *= int(pyLib.memory.memory().readMemory(operand), base= 2)
        elif opcode == "DIV":
            self.actualProcess.accumulator //= int(pyLib.memory.memory().readMemory(operand), base= 2)
        elif opcode == "REM":
            self.actualProcess.accumulator %= int(pyLib.memory.memory().readMemory(operand), base= 2)
        elif opcode == "AND":
            self.actualProcess.accumulator &= int(pyLib.memory.memory().readMemory(operand), base= 2)
        elif opcode == "ORR":
            self.actualProcess.accumulator |= int(pyLib.memory.memory().readMemory(operand), base= 2)
        elif opcode == "NOT":
            self.actualProcess.accumulator = ~ self.actualProcess.accumulator
        elif opcode == "XOR":
            self.actualProcess.accumulator ^= int(pyLib.memory.memory().readMemory(operand), base= 2)
        elif opcode == "TXT":
            number = str(self.actualProcess.accumulator)
            textLen = len(number)
            word = toBin(textLen, 8)
            for i in range(textLen):
                char = toBin(ord(number[i]), 8)
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
            self.actualProcess.accumulator = number
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
            if self.actualProcess.accumulator - int(pyLib.memory.memory().readMemory(operand), base= 2) == 0:
                self.actualProcess.flagZ = 1
            if self.actualProcess.accumulator - int(pyLib.memory.memory().readMemory(operand), base= 2) < 0:
                self.actualProcess.flagN = 1
        elif opcode == "BEQ":
            if self.actualProcess.flagZ == 1:
                self.actualProcess.programCounter = operand
                return
        elif opcode == "BNE":
            if self.actualProcess.flagZ == 0:
                self.actualProcess.programCounter = operand
                return
        elif opcode == "JMP":
            self.actualProcess.programCounter = operand
            return
        elif opcode == "SET":
            bits = toBin(operand, 8)[-3:]
            self.actualProcess.flagI = int(bits[0])
            self.actualProcess.flagN = int(bits[1])
            self.actualProcess.flagZ = int(bits[2])
        self.actualProcess.programCounter += 1
        return

def cpu():
    if _cpu._instance is None:
        _cpu._instance = _cpu()
    return _cpu._instance