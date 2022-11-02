import os

from rich import box
from rich.style import Style
from rich.console import RenderableType
from rich.text import Text
from rich.table import Table

from textual import events
from textual.reactive import Reactive
from textual.widget import Widget

from pyLib.infoLists import validCommands, keysToIgnore

import pyLib.memory
import pyLib.assembler
import pyLib.interface
import pyLib.virtualDisc
import pyLib.processAdmin

class _cmdLine(Widget):
    _instance = None
    
    cmdHeight= 9
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
    
    def printExit(self, text: str):
        self.printedHistory.append(
            Text(text, style= self.printStyle)
        )
        self.refresh()
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
            self.printError("Arquivo não é '.qck'")
            return
        if not os.path.exists("./root/" + cmd[1]):
            self.printError("Arquivo não existe")
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
            self.printError("Arquivo não é '.fita'")
            return
        if not os.path.exists("./root/" + cmd[1]):
            self.printError("Arquivo não existe")
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
        if len(cmd) != 2:
            self.printError("Argumentos errados")
            return
        if not pyLib.memory.memory().isLoaded(cmd[1]):
            self.printError("Aplicativo não carregado na memória")
            return
        pyLib.memory.memory().dumpMemory(cmd[1])
        self.printSuccess("Dumped " + cmd[1] + " para dump_" + cmd[1] + ".txt")
        return
    
    def cmdRun(self, cmd: iter):
        if len(cmd) != 2:
            self.printError("Argumentos errados")
            return
        if pyLib.processAdmin.processAdmin().isProcessAdded(cmd[1]):
            self.printError("Aplicativo já está em execução")
            return
        if not pyLib.memory.memory().isLoaded(cmd[1]):
            self.cmdLoad(cmd)
        appInfo = pyLib.memory.memory().getAppInfo(cmd[1])
        pyLib.processAdmin.processAdmin().createProcess(cmd[1], "Pronto", appInfo[0])
        self.printSuccess("Adicionado " + cmd[1] + " a fila de processos") 
        return
    
    def cmdCreate(self, cmd: iter):
        self.printError("Comando não implementado")
        return
    
    def cmdEdit(self, cmd: iter):
        # try:
        #     pyLib.assembler.assemble("algo")
        # except pyLib.assembler.MyValidationError as exception:
        #     self.printError(exception.args[0])
        self.printError("Comando não implementado")
        # self.printError(str(list(proc.name for proc in pyLib.processAdmin.processAdmin().processList)))
        return
    
    def cmdDelete(self, cmd: iter):
        if len(cmd) == 2:
            if pyLib.virtualDisc.virtualDisc().deleteFile(cmd[1]):
                self.printSuccess("Deleted " + cmd[1])
                pyLib.interface.interface().refresh()
                return
            self.printError("Falha ao deletar: " + cmd[1])
            return
        self.printError("Argumentos errados")
        return
    
    def cmdClear(self, cmd: iter):
        if len(cmd) == 1:
            self.printedHistory = list()
            return
        self.printError("Argumentos errados")
        
    def commands(self, cmd: iter):
        cmd[0] = cmd[0].lower()
        if validCommands.count(cmd[0]) == 0:
            self.printError("Comando inexistente")
            return
        if cmd[0] == "assemble":
            self.cmdAssemble(cmd)
        elif cmd[0] == "load":
            self.cmdLoad(cmd)
        elif cmd[0] == "unload":
            self.cmdUnload(cmd)
        elif cmd[0] == "dump":
            self.cmdDump(cmd)
        elif cmd[0] == "run":
            self.cmdRun(cmd)
        elif cmd[0] == "create":
            self.cmdCreate(cmd)
        elif cmd[0] == "edit":
            self.cmdEdit(cmd)
        elif cmd[0] == "delete":
            self.cmdDelete(cmd)
        elif cmd[0] == "clear":
            self.cmdClear(cmd)
    
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