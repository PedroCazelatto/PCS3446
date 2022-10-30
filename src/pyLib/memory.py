import os

from rich.style import Style
from rich.panel import Panel
from rich.console import RenderableType
from rich.tree import Tree
from rich.table import Table
from rich.progress import DownloadColumn, Progress, BarColumn

from textual.widget import Widget

# Memory is addressed by words

class _memory(Widget):
    _instance = None
    
    totalSpace = 2**18
    filledSpace = 0
    unusedSpace = [[0, totalSpace]] # [Addr , freeSpace at Addr]
    
    actualMemory = list()
    for i in range(totalSpace):
        actualMemory.append(32 * '0')
    
    loadedAppsTree = Tree("Memória Principal")
    loadedAppsList = list()
    loadedAppsInfo = list()
    
    filledBar = Progress(
        BarColumn(bar_width= None),
        DownloadColumn(binary_units= True),
        auto_refresh= False, expand= True
    )
    filledBarTask = filledBar.add_task("", total= totalSpace*4)
    
    memoryRenderable = Table(
        expand= True,
        pad_edge= False,
        show_header= False,
        show_edge= False
    )
    memoryRenderable.add_row(filledBar)
    memoryRenderable.add_row(loadedAppsTree)
    
    def readMemory(self, address: int) -> str:
        return self.actualMemory[address]
    
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

    # Missing LOADER call
    def loadApp(self, appName: str) -> bool:
        if self.loadedAppsList.count(appName) == 0:
            if os.path.exists("./root/" + appName):
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
                    return False
                self.loadedAppsList.append(appName)
                self.loadedAppsInfo.append(
                    fileLen,
                    memoryStartPos
                )
                for i in range(fileLen):
                    self.actualMemory[memoryStartPos + i] = file[i]
                self.filledSpace += fileLen
                self.refresh()
                return True
        return False
    
    def unloadApp(self, appName: str) -> bool:
        if self.loadedAppsList.count(appName) == 0:
            return False
        if appName == "loader":
            return False
        index = self.loadedAppsList.index(appName)
        self.loadedAppsList.remove(appName)
        self.unusedSpace.append(self.loadedAppsInfo[index])
        self.memoryUnifier()
        self.filledSpace -= self.loadedAppsInfo[index][0]
        self.loadedAppsInfo.pop(index)
        self.refresh()
        return True
    
    def render(self) -> RenderableType:
        self.filledBar.update(self.filledBarTask, completed= self.filledSpace*4)
        for i, app in enumerate(self.loadedAppsList):
            self.loadedAppsTree.add(app + " [" + self.getBinaryWithSuffix(self.loadedAppsInfo[i][0]) + "]")
        return Panel(self.memoryRenderable,
                     title= "Aplicativos carregados",
                     border_style= Style(color= "bright_cyan"))

def memory():
    if _memory._instance is None:
        _memory._instance = _memory()
    return _memory._instance