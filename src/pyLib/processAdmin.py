from rich.text import Text
from rich.style import Style
from rich.panel import Panel
from rich.table import Table
from rich.console import RenderableType

from textual.widget import Widget

from pyLib.configs import *

import pyLib.cmdLine
import pyLib.processor
import pyLib.generalProcess

class _processAdmin(Widget):
    _instance = None
    cyclesRemaining = 5
    cyclesToChange = 10
    isLoading = False
    processList = list()
    
    boldStyle = Style(bold= True)
    
    waitingProcess = pyLib.generalProcess.process("Espera", "Bloqueado", -1)
    
    def clockRise(self):
        if not self.isLoading:
            self.countCycles()
        pyLib.processor.cpu().processInstruction()
        self.refresh()
        return
    
    def countCycles(self):
        if pyLib.processor.cpu().getProcess().name == "Espera":
            self.executeNextProcess()
            return
        self.cyclesRemaining -= 1
        if self.cyclesRemaining == 0:
            self.cyclesRemaining = self.cyclesToChange
            self.stopCurrentProcess()
            self.executeNextProcess()
        return
    
    def isProcessAdded(self, processName):
        if pyLib.processor.cpu().getProcess().name == processName:
            return True
        for process in self.processList:
            if process.name == processName:
                return True
        return False
    
    def changeProcessState(self, processName: str, newState: str):
        for idx, proc in enumerate(self.processList):
            if proc.name == processName:
                self.processList[idx].state = newState
                self.sortProcess()
                return
        return
    
    def createProcess(self, processName: str, state: str, baseAddress: int):
        self.processList.insert(0, pyLib.generalProcess.process(processName, state, baseAddress))
        self.sortProcess()
        return
    
    def countExecutingProcess(self):
        total = 0
        for process in self.processList:
            if process.state == "Executando":
                total += 1
        return total
    
    def selectExecutionProcess(self):
        for i in range(min(multiprogrammingDegree, len(self.processList))):
            if self.processList[i].state == "Pronto":
                self.processList[i].state = "Executando"
        return
    
    def executeNextProcess(self):
        if len(self.processList) == 0:
            pyLib.processor.cpu().setProcess(self.waitingProcess)
            return
        if self.countExecutingProcess != multiprogrammingDegree:
            self.selectExecutionProcess()
        if self.processList[0].state != "Executando":
            pyLib.processor.cpu().setProcess(self.waitingProcess)
            return
        pyLib.processor.cpu().setProcess(self.processList[0])
        self.processList.pop(0)
        return
    
    def stopCurrentProcess(self):
        process = pyLib.processor.cpu().getProcess()
        if process.name == "Loader":
            self.isLoading = False
            self.processList.append(process)
        else:
            if not process.halted:
                self.processList.append(process)
                self.sortProcess()
        pyLib.processor.cpu().setProcess(self.waitingProcess)
        return
    
    def runLoader(self):
        self.isLoading = True
        self.stopCurrentProcess()
        for idx, process in enumerate(self.processList):
            if process.name == "Loader":
                loaderIdx = idx
                break
        pyLib.processor.cpu().setProcess(pyLib.generalProcess.process("Loader", "Bloqueado", 0))
        self.processList.pop(loaderIdx)
        return
    
    def sortProcess(self):
        executingProcess = list()
        readyProcess = list()
        awaitingProcess = list()
        blockedProcess = list()
        for process in self.processList:
            if process.state == "Executando":
                executingProcess.append(process)
            elif process.state == "Pronto":
                readyProcess.append(process)
            elif process.state == "Entrada":
                awaitingProcess.append(process)
            else:
                blockedProcess.append(process)
        self.processList = executingProcess + readyProcess + awaitingProcess + blockedProcess
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
        actualProcess = pyLib.processor.cpu().getProcess()
        if actualProcess.name == "Espera":
            renderable.add_row("Esperando", "0")
            return renderable
        if actualProcess.name == "Loader":
            renderable.add_row("Loading", "-")
            return renderable
        renderable.add_row(actualProcess.name, str(self.cyclesRemaining))
        return renderable
    
    def getProcessRenderable(self, process: pyLib.generalProcess.process) -> Table:
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
            show_edge= False,
            style= Style(color= "bright_cyan", bold= True)
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