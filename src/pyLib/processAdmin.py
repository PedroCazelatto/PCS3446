from rich.text import Text
from rich.tree import Tree
from rich.style import Style
from rich.panel import Panel
from rich.table import Table
from rich.layout import Layout
from rich.console import RenderableType

from textual.widget import Widget

import pyLib.processor

# possibleStates = ["Pronto", "Aguardando Entrada", "Bloqueado"]

class process():
    def __init__(self, processName: str, baseState: str, baseAddress: int):
        self.name = processName
        self.state = baseState
        self.programCounter = baseAddress
        self.accumulator = 0
        self.halted = False
        self.flagI = 0
        self.flagN = 0
        self.flagZ = 0
        return
    
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

class _processAdmin(Widget):
    _instance = None
    cyclesToChange = 5
    isLoading = False
    processList = list()
    
    boldStyle = Style(bold= True)
    
    waitingProcess = process("Espera", "Bloqueado", -1)
    actualProcess = waitingProcess
    
    def clockRise(self):
        if not self.isLoading:
            self.countCycles()
        pyLib.processor.cpu().processInstruction()
        return
    
    def countCycles(self):
        self.cyclesToChange -= 1
        if self.cyclesToChange == 0:
            if self.actualProcess.name == "Espera":
                self.cyclesToChange = 2
            else:
                self.cyclesToChange = 10
            self.changeProcess()
        self.refresh()
        return
    
    def changeProcess(self):
        if self.actualProcess.name == "Loader":
            self.isLoading = False
            self.processList.append(process("Loader", "Bloqueado", 0))
        self.actualProcess.setStatus(pyLib.processor.cpu().getStatus())
        if self.processList[0].state == "Pronto":
            nextProcess = self.processList[0]
            self.processList.pop(0)
            if not self.actualProcess.halted:
                self.processList.append(self.actualProcess)
                self.sortProcess()
        else:
            if self.actualProcess.state == "Aguardando Entrada" or self.actualProcess.halted:
                nextProcess = self.waitingProcess
            else:
                nextProcess = self.actualProcess
        self.actualProcess = nextProcess
        self.refresh()
        return
    
    def addProcess(self, processName: str, state: str, baseAddress: int):
        self.processList.insert(0, process(processName, state, baseAddress))
        return
    
    def runLoader(self):
        self.isLoading = True
        if self.actualProcess.name != "Espera":
            self.actualProcess.setStatus(pyLib.processor.cpu().getStatus())
            self.processList.append(self.actualProcess)
            self.sortProcess()
        for idx, process in enumerate(self.processList):
            if process.name == "Loader":
                nextProcessIdx = idx
                break
        self.actualProcess = self.processList[nextProcessIdx]
        self.processList.pop(idx)
        pyLib.processor.cpu().setStatus([0, 0, False, 0, 0, 0])
        return
    
    def sortProcess(self):
        readyProcess = list()
        awaitingProcess = list()
        blockedProcess = list()
        for process in self.processList:
            if process.state == "Pronto":
                readyProcess.append(process)
            elif process.state == "Aguardando Entrada":
                awaitingProcess.append(process)
            else:
                blockedProcess.append(process)
        self.processList = readyProcess + awaitingProcess + blockedProcess
        return
    
    def getActualProcessRenderable(self) -> Table:
        renderable = Table(
            expand= True,
            pad_edge= False,
            show_header= False,
            show_edge= False,
            box= None
        )
        renderable.add_column(justify= "center", ratio= 2)
        renderable.add_column(justify= "center", ratio= 1)
        if self.actualProcess.name == "Espera":
            renderable.add_row("Esperando", "0")
            return renderable
        if self.actualProcess.name == "Loader":
            renderable.add_row("Loading", "-")
            return renderable
        renderable.add_row(self.actualProcess.name, str(self.cyclesToChange))
        return renderable
    
    def getProcessRenderable(self, process: process) -> Table:
        renderable = Table(
            expand= True,
            pad_edge= False,
            show_header= False,
            show_edge= False,
            box= None
        )
        renderable.add_column(justify= "center", ratio= 2)
        renderable.add_column(justify= "center", ratio= 1)
        renderable.add_row(process.name, process.state)
        return renderable
    
    def getRenderable(self) -> Table:
        adminTable = Table(
            expand= True,
            pad_edge= False,
            show_header= False,
            show_edge= False
        )
        adminTable.add_column(justify= "center")
        adminTable.add_row(Text("Processo Atual:", style= self.boldStyle))
        adminTable.add_row(self.getActualProcessRenderable(), end_section= True)
        adminTable.add_row("Fila de Processos:", style= self.boldStyle)
        for process in self.processList:
            adminTable.add_row(self.getProcessRenderable(process))
        return adminTable
    
    def render(self) -> RenderableType:
        return Panel(self.getRenderable(),
                     title= "Administrador de Processos",
                     border_style= Style(color= "bright_cyan"))

def processAdmin():
    if _processAdmin._instance is None:
        _processAdmin._instance = _processAdmin()
    return _processAdmin._instance