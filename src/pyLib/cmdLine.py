import os
import time

from rich import box
from rich.style import Style
from rich.console import RenderableType
from rich.text import Text
from rich.table import Table
from rich.layout import Layout

from textual import events
from textual.reactive import Reactive
from textual.widget import Widget

import pyLib.memory
import pyLib.assembler
import pyLib.interface
import pyLib.virtualDisc

from pyLib.infoLists import validCommands, keysToIgnore

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
        return
    
    def printError(self, text: str):
        self.printedHistory.append(
            Text(text, style= self.errorStyle)
        )
        return
    
    def printSuccess(self, text: str):
        self.printedHistory.append(
            Text(text, style= self.goodStyle)
        )
        return
    
    def cmdAssemble(self, cmd: iter):
        if len(cmd) == 2:
            returned = pyLib.assembler.assemble(cmd[1])
            if returned[0]:
                self.printSuccess(returned[1])
                return
            self.printError(returned[1])
            return
        self.printError("Argumentos errados")
        return
    
    def cmdLoad(self, cmd: iter):
        if len(cmd) == 2:
            returned = pyLib.memory.memory().loadApp(cmd[1])
            if returned[0]:
                self.printSuccess(returned[1])
                return
            self.printError(returned[1])
            return
        self.printError("Argumentos errados")
        return
    
    def cmdUnload(self, cmd: iter):
        if len(cmd) == 2:
            if pyLib.memory.memory().unloadApp(cmd[1]):
                self.printSuccess("Unloaded " + cmd[1])
                return
            self.printError("Falha ao descarregar: " + cmd[1])
            return
        self.printError("Argumentos errados")
        return
    
    def cmdRun(self, cmd: iter):
        self.printError("Comando não implementado")
        return
    
    def cmdCreate(self, cmd: iter):
        self.printError("Comando não implementado")
        return
    
    def cmdEdit(self, cmd: iter):
        self.printError("Comando não implementado")
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