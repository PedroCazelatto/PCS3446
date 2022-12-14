import os
import time

from rich import box
from rich.text import Text
from rich.style import Style
from rich.table import Table
from rich.console import RenderableType

from textual import events
from textual.reactive import Reactive
from textual.widget import Widget

from pyLib.usefulFuncs import *
from pyLib.infoLists import validCommands, keysToIgnore

import pyLib.memory
import pyLib.assembler
import pyLib.interface
import pyLib.virtualDisc
import pyLib.processAdmin

class _cmdLine(Widget):
    _instance = None
    
    cmdHeight= 7
    line = Reactive(Text("cmd> "))
    cmdText = ""
    cmdRight = ""
    history = [""]
    printedHistory = list()
    x = 0
    y = 0
    errorStyle = Style(color= "red1", bold= True)
    goodStyle = Style(color= "green1", bold= True)
    printStyle = Style(color= "cadet_blue", bold= True)
    
    linesToInput = 0
    inputAddresses = list()
        
    def on_key(self, event: events.Key):
        if keysToIgnore.count(event.key) == 1:
            pass
        elif event.key == "ctrl+h":
            self.cmdText = self.cmdText[:self.y-1] + self.cmdText[self.y:]
            self.y -= 1
        elif event.key == "delete":
            self.cmdText = self.cmdText[:self.y] + self.cmdText[self.y+1:]
        elif event.key == "ctrl+i":
            elements = [elem[:self.y] for elem in validCommands]
            if elements.count(self.cmdText[:self.y]) == 1:
                cmdNumber = elements.index(self.cmdText[:self.y])
                self.cmdText = self.cmdText[:self.y] + validCommands[cmdNumber][self.y:] + self.cmdText[self.y:]
                self.y += len(validCommands[cmdNumber][self.y:])
        elif event.key == "enter":
            self.cmdText = self.cmdText + self.cmdRight
            if (not self.cmdText.isspace()) and self.cmdText:
                self.history.append(self.cmdText)
                self.printedHistory.append(self.cmdText)
                self.commands(self.cmdText.split())
            self.cmdText = ""
            self.cmdRight = ""
            self.x = 0
            self.y = 0
        elif event.key == "up":
            if self.x != -len(self.history)+1:
                self.x -= 1
                self.cmdText = self.history[self.x]
                self.y = len(self.cmdText)
        elif event.key == "down":
            if self.x != 0:
                self.x += 1
                self.cmdText = self.history[self.x]
                self.y = len(self.cmdText)
        elif event.key == "left":
            if self.y != 0:
                self.y -= 1
        elif event.key == "right":
            if self.y != len(self.cmdText):
                self.y += 1
        else:
            self.cmdText = self.cmdText[:self.y] + event.key + self.cmdText[self.y:]
            self.y += 1
        self.line = Text("cmd> ").append(self.cmdText[:self.y]).append("_", style=Style(blink=True)).append(self.cmdText[self.y:])
    
    def inputFromFile(self, inputFile: str, operand: int):
        lines = list()
        with open(inputFile) as file:
            for line in file:
                lines.append(line[:-1])
        for idx, line in enumerate(lines):
            if line[0] != '*':
                try:
                    int(line)
                except:
                    lines[idx] = '*' + line
                    continue
                actualInput = line
                lines[idx] = '*' + line
                break
        size = int(pyLib.memory.memory().readMemory(operand)[:8], base= 2)
        wordsToSave = toASCII(actualInput, size)
        for idx, word in enumerate(wordsToSave):
            pyLib.memory.memory().writeMemory(operand + idx, word)
        with open(inputFile, 'w') as file:
            for line in lines:
                file.write(line + '\n')
    
    def inputFromCmd(self, text: str):
        try:
            int(text)
        except:
            self.printError("Digite apenas um n??mero")
            return
        operand, name = self.inputAddresses.pop(0)
        size = int(pyLib.memory.memory().readMemory(operand)[:8], base= 2)
        wordsToSave = toASCII(text, size)
        for idx, word in enumerate(wordsToSave):
            pyLib.memory.memory().writeMemory(operand + idx, word)
        if pyLib.processAdmin.processAdmin().isProcessAdded(name):
            pyLib.processAdmin.processAdmin().changeProcessState(name, "Pronto")
        else:
            self.printError("Processo " + name + " desapareceu!")
        return
    
    def printOutput(self, appName: str, text: str):
        outputFile = pyLib.memory.memory().getAppInfo(appName)[3]
        if outputFile == '':
            self.printedHistory.append(
                Text(text, style= self.printStyle)
            )
            self.refresh()
            return
        currentTime = time.strftime("%H:%M:%S", time.localtime())
        with open(outputFile, 'a') as file:
            file.write(currentTime + " " + text + "\n")
        return
    
    def printError(self, text: str):
        self.printedHistory.append(
            Text(text, style= self.errorStyle)
        )
        self.refresh()
        return
    
    def printSuccess(self, text: str):
        self.printedHistory.append(
            Text(text, style= self.goodStyle)
        )
        self.refresh()
        return
    
    def cmdAssemble(self, cmd: iter):
        if len(cmd) != 2:
            self.printError("Argumentos errados")
            return
        if cmd[1][-4:] != ".qck":
            self.printError("Arquivo n??o ?? '.qck'")
            return
        if not os.path.exists("./root/" + cmd[1]):
            self.printError("Arquivo n??o existe")
            return
        out = pyLib.assembler.assemble("./root/" + cmd[1])
        if not out[0]:
            self.printError("Erro: " + out[1])
            return
        self.printSuccess(out[1])
        return
    
    def cmdLoad(self, cmd: iter):
        if len(cmd) != 2:
            self.printError("Argumentos errados")
            return
        if cmd[1][-5:] != ".fita":
            self.printError("Arquivo n??o ?? '.fita'")
            return
        if not os.path.exists("./root/" + cmd[1]):
            self.printError("Arquivo n??o existe")
            return
        out = pyLib.memory.memory().loadApp(cmd[1])
        if not out[0]:
            self.printError("Erro: " + out[1])
            return
        self.printSuccess(out[1])
        return
    
    def cmdUnload(self, cmd: iter):
        if len(cmd) != 2:
            self.printError("Argumentos errados")
            return
        out = pyLib.memory.memory().unloadApp(cmd[1])
        if not out[0]:
            self.printError("Erro: " + out[1])
            return
        self.printSuccess(out[1])
        return
    
    def cmdDump(self, cmd: iter):
        if len(cmd) == 1:
            self.printError("Ainda n??o implementado")
            return
        if len(cmd) != 2:
            self.printError("Argumentos errados")
            return
        if not pyLib.memory.memory().isLoaded(cmd[1]):
            self.printError("Aplicativo n??o carregado na mem??ria")
            return
        pyLib.memory.memory().dumpMemory(cmd[1])
        self.printSuccess("Dumped " + cmd[1] + " para dump_" + cmd[1] + ".txt")
        return
    
    def cmdRun(self, cmd: iter):
        if len(cmd) != 2:
            self.printError("Argumentos errados")
            return
        if pyLib.processAdmin.processAdmin().isProcessAdded(cmd[1]):
            self.printError("Aplicativo j?? est?? em execu????o")
            return
        if not pyLib.memory.memory().isLoaded(cmd[1]):
            self.cmdLoad(["load", cmd[1] + ".fita"])
        if not pyLib.memory.memory().isLoaded(cmd[1]):
            return
        appInfo = pyLib.memory.memory().getAppInfo(cmd[1])
        pyLib.processAdmin.processAdmin().createProcess(cmd[1], "Pronto", appInfo[0])
        self.printSuccess("Adicionado " + cmd[1] + " a fila de processos") 
        return
    
    def cmdSet(self, cmd: iter):
        if len(cmd) != 4:
            self.printError("Argumentos errados")
            return
        cmd[2] = cmd[2].lower()
        if cmd[2] != "in" and cmd[2] != "out":
            self.printError("Defina in ou out")
            return
        if not pyLib.memory.memory().isLoaded(cmd[1]):
            self.printError("Aplicativo n??o carregado na mem??ria")
            return
        if cmd[2] == "in":
            if cmd[3].lower() == "cmd":
                pyLib.memory.memory().setAppInput(cmd[1], '')
                self.printSuccess("Entrada de " + cmd[1] + " a partir do CMD")
                return
            if not os.path.exists("./root/" + cmd[3]):
                self.printError("Arquivo n??o existe!")
                return
            pyLib.memory.memory().setAppInput(cmd[1], "./root/" + cmd[3])
            self.printSuccess("Entrada de " + cmd[1] + " a partir de " + cmd[3])
            return
        if cmd[2] == "out":
            if cmd[3].lower() == "cmd":
                pyLib.memory.memory().setAppOutput(cmd[1], '')
                self.printSuccess("Sa??da de " + cmd[1] + " a partir do CMD")
                return
            if not os.path.exists("./root/" + cmd[3]):
                with open("./root/" + cmd[3], 'w'):
                    pass
                return
            pyLib.memory.memory().setAppOutput(cmd[1], "./root/" + cmd[3])
            self.printSuccess("Sa??da de " + cmd[1] + " a partir de " + cmd[3])
            return
        return
            
    def cmdCreate(self, cmd: iter):
        if len(cmd) != 2:
            self.printError("Argumentos errados")
            return
        if os.path.exists("./root/" + cmd[1]):
            self.printError("Arquivo j?? existe")
            return
        out = pyLib.virtualDisc.virtualDisc().createFile(cmd[1])
        pyLib.interface.interface().refresh()
        if not out[0]:
            self.printError("Erro: " + out[1])
            return
        self.printSuccess(out[1])
        return
    
    def cmdEdit(self, cmd: iter):
        self.printError("Comando n??o implementado")
        return
    
    def cmdDelete(self, cmd: iter):
        if len(cmd) != 2:
            self.printError("Argumentos errados")
            return
        if not os.path.exists("./root/" + cmd[1]):
            self.printError("Arquivo n??o existe")
            return
        out = pyLib.virtualDisc.virtualDisc().deleteFile(cmd[1])
        pyLib.interface.interface().refresh()
        if not out[0]:
            self.printError("Erro: " + out[1])
            return
        self.printSuccess(out[1])
        return
    
    def cmdClear(self, cmd: iter):
        if len(cmd) == 1:
            self.printedHistory = list()
            return
        self.printError("Argumentos errados")
        
    def commands(self, cmd: iter):
        cmd[0] = cmd[0].lower()
        if validCommands.count(cmd[0]) == 0:
            if len(self.inputAddresses) == 0:
                self.printError("Comando inexistente")
                return
            if len(cmd) != 1:
                self.printError("Digite apenas um n??mero")
                return
            self.inputFromCmd(cmd[0])
        elif cmd[0] == "assemble":
            self.cmdAssemble(cmd)
        elif cmd[0] == "load":
            self.cmdLoad(cmd)
        elif cmd[0] == "unload":
            self.cmdUnload(cmd)
        elif cmd[0] == "dump":
            self.cmdDump(cmd)
        elif cmd[0] == "run":
            self.cmdRun(cmd)
        elif cmd[0] == "set":
            self.cmdSet(cmd)
        elif cmd[0] == "create":
            self.cmdCreate(cmd)
        elif cmd[0] == "edit":
            self.cmdEdit(cmd)
        elif cmd[0] == "delete":
            self.cmdDelete(cmd)
        elif cmd[0] == "clear":
            self.cmdClear(cmd)
        return
    
    def on_focus(self) -> None:
        self.line = Text("cmd> ").append(self.cmdText).append("_", style=Style(blink=True))
        
    def on_blur(self) -> None:
        self.line = self.line[:-1]

    def render(self) -> RenderableType:
        grid = Table(
            show_header= False,
            expand= True,
            box= box.HEAVY,
            style= Style(color= "blue1", bold= True)
        )
        
        for x in range(self.cmdHeight):
            if x >= self.cmdHeight - len(self.printedHistory):
                grid.add_row(self.printedHistory[-self.cmdHeight + x])
            else:
                grid.add_row("")
        grid.add_row(self.line)
        return grid

def cmdLine():
    if _cmdLine._instance is None:
        _cmdLine._instance = _cmdLine()
    return _cmdLine._instance