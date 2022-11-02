import os

from rich.style import Style
from rich.panel import Panel
from rich.console import RenderableType
from rich.tree import Tree
from rich.table import Table
from rich.progress import DownloadColumn, Progress, BarColumn

from textual.widget import Widget

from pyLib.configs import *
from pyLib.usefulFuncs import *

import pyLib.assembler
import pyLib.processAdmin

# Memory is addressed by words

class _memory(Widget):
    _instance = None
    
    totalSpace = 2**(memoryAddressBits)
    filledSpace = 0
    unusedSpace = [[0, totalSpace]] # [Addr , freeSpace at Addr]
    
    filledBar = Progress(
        BarColumn(bar_width= None),
        DownloadColumn(binary_units= True),
        auto_refresh= False, expand= True
    )
    filledBarTask = filledBar.add_task("", total= totalSpace*4)
    
    actualMemory = list()
    for i in range(totalSpace):
        actualMemory.append(32 * '0')
    
    loadedAppsList = list()
    loadedAppsInfo = list()
    
    def isLoaded(self, appName: str):
        if self.loadedAppsList.count(appName) == 0:
            return False
        return True
    
    def getAppInfo(self, appName: str):
        idx = self.loadedAppsList.index(appName)
        return self.loadedAppsInfo[idx]
    
    def readMemory(self, address: int) -> str:
        return self.actualMemory[address]
    
    def writeMemory(self, address: int, value: int):
        self.actualMemory[address] = toBin(value, 32)
        return
    
    def dumpMemory(self, appName: str):
        start, length = self.getAppInfo(appName)
        with open("./root/dump_" + appName + ".txt", 'w') as dumping:
            for i in range(length):
                dumping.write(self.readMemory(start + i) + '\n')
        return
    
    def memoryUnifier(self):
        self.unusedSpace.sort()
        for i in range(len(self.unusedSpace)-1):
            currAddr = self.unusedSpace[i][0]
            freeSpace = self.unusedSpace[i][1]
            nextAddr = self.unusedSpace[i+1][0]
            if currAddr + freeSpace == nextAddr:
                self.unusedSpace[i][1] += self.unusedSpace[i+1][1]
                self.unusedSpace.pop(i+1)
    
    def getBinaryWithSuffix(self, bytes: int):
        if bytes < 1024:
            return str(bytes) + " B"
        return str(bytes/1024) + " KiB"
    
    # Reads binary and return list of instructions
    def parse_binary(self, filePath: str):
        instructions = list()
        if os.path.exists(filePath):
            with open(filePath) as file:
                for line in file:
                    instructions.append(line[:-1])
        return instructions
    
    def loadLoader(self) -> bool:
        if not os.path.exists("loader.fita"):
            if not os.path.exists("loader.qck"):
                return False
            pyLib.assembler.assemble("loader.qck")
        file = self.parse_binary("loader.fita")
        fileLen = len(file)
        memoryStartPos = 0
        self.unusedSpace[0][0] += fileLen
        self.unusedSpace[0][1] -= fileLen
        self.loadedAppsList.append("Loader")
        self.loadedAppsInfo.append([
            memoryStartPos,
            fileLen
        ])
        for i in range(fileLen):
            self.actualMemory[memoryStartPos + i] = file[i]
        self.filledSpace += fileLen
        self.refresh()
        pyLib.processAdmin.processAdmin().createProcess("Loader", "Bloqueado", 0)
        return True

    def loadApp(self, appName: str):
        if self.isLoaded(appName):
            return [False, "Aplicativo já está na memória"]
        # if os.path.exists("./root/" + appName):
        file = self.parse_binary("./root/" + appName)
        fileLen = len(file)
        memoryStartPos = -1
        for idx, seq in enumerate(self.unusedSpace):
            if seq[1] >= fileLen:
                memoryStartPos = seq[0]
                if seq[1] == fileLen:
                    self.unusedSpace.pop(idx)
                else:
                    self.unusedSpace[idx][0] += fileLen
                    self.unusedSpace[idx][1] -= fileLen
                break
        if memoryStartPos == -1:
            return [False, "Sem espaço na memória"]
        self.loadedAppsList.append(appName[:-5])
        self.loadedAppsInfo.append([
            memoryStartPos,
            fileLen
        ])
        for i in range(fileLen):
            self.actualMemory[memoryStartPos + i] = file[i]
        self.filledSpace += fileLen
        self.refresh()
        self.actualMemory[38] = toBin(memoryStartPos, 32)
        self.actualMemory[39] = toBin(fileLen, 32)
        pyLib.processAdmin.processAdmin().runLoader()
        return [True, "Carregando " + appName[:-5] + " na memória"]
    
    def unloadApp(self, appName: str):
        if not self.isLoaded(appName):
            return [False, "Aplicativo não está na memória"]
        if appName == "Loader":
            return [False, "Não é possivel descarregar o Loader"]
        index = self.loadedAppsList.index(appName)
        self.loadedAppsList.remove(appName)
        self.unusedSpace.append(self.loadedAppsInfo[index])
        self.memoryUnifier()
        self.filledSpace -= self.loadedAppsInfo[index][1]
        self.loadedAppsInfo.pop(index)
        self.refresh()
        return [True, "Descarregado " + appName]
    
    def getRenderable(self) -> Table:
        loadedAppsTree = Tree("Memória Principal")
        for i, app in enumerate(self.loadedAppsList):
            loadedAppsTree.add(app + " [" + self.getBinaryWithSuffix(self.loadedAppsInfo[i][1]*4) + "]")
        renderable = Table(
            expand= True,
            pad_edge= False,
            show_header= False,
            show_edge= False,
            box= None
        )
        renderable.add_row(self.filledBar)
        renderable.add_row(loadedAppsTree)
        return renderable
    
    def render(self) -> RenderableType:
        self.filledBar.update(self.filledBarTask, completed= self.filledSpace*4)
        return Panel(self.getRenderable(),
                     title= "Memória Simulada",
                     border_style= Style(color= "bright_cyan"))

def memory():
    if _memory._instance is None:
        _memory._instance = _memory()
    return _memory._instance