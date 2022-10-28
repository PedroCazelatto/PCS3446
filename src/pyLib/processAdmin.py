from rich.text import Text
from rich.tree import Tree
from rich.style import Style
from rich.panel import Panel
from rich.table import Table
from rich.layout import Layout
from rich.console import RenderableType

from textual.widget import Widget

# possibleStates = ["Pronto", "Aguardando Entrada", "Bloqueado"]

class process():
    
    def __init__(self, processName: str):
        self.name = processName
        self.state = "Pronto"
        return
    
    def changeState(self, newState: str):
        self.state = newState
        return

class _processAdmin(Widget):
    _instance = None
    cyclesToChange = 5
    isLoading = False
    processList = list()
    
    boldStyle = Style(bold= True)
    
    actualProcess = "Teste"
    
    def clockRise(self):
        # call clockRise at processor
        if self.isLoading:
            return
        self.countCycles()
        return
    
    def countCycles(self):
        self.cyclesToChange -= 1
        if self.cyclesToChange == 0:
            self.cyclesToChange = 5
        self.refresh()
        return
    
    def addProcess(self, processName: str):
        self.processList.insert(0, process(processName))
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
        if self.actualProcess == "Espera":
            renderable.add_row("Esperando", "0")
            return renderable
        renderable.add_row(self.actualProcess, str(self.cyclesToChange))
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