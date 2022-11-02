from rich import box
from rich.align import Align
from rich.style import Style
from rich.panel import Panel
from rich.console import RenderableType
from rich.table import Table
from rich.text import Text

from textual.widget import Widget

from pyLib.usefulFuncs import *
import pyLib.processor
import pyLib.generalProcess

class _cpuVariables(Widget):
    _instance = None
    
    varList = [
        Text("Acumulador", justify= "center"),
        Text("Contador de Programa", justify= "center"),
        Text("Flags (I N Z)", justify= "center"),
    ]
    
    def render(self) -> RenderableType:
        variables = [
            toHex(pyLib.processor.cpu().actualProcess.accumulator, 8),
            str(pyLib.processor.cpu().actualProcess.programCounter),
            str(pyLib.processor.cpu().actualProcess.flagI) + " " + str(pyLib.processor.cpu().actualProcess.flagN) + " " + str(pyLib.processor.cpu().actualProcess.flagZ)
        ]
        varTable = Table(
            box= box.HEAVY,
            expand= True,
            show_header= False,
            show_edge= False,
            style= Style(color= "bright_cyan", bold= True)
        )
        for i in range(len(self.varList)):
            varTable.add_row(self.varList[i])
            varTable.add_row(Align.center(variables[i]), end_section= True)
        return Panel(varTable,
                     title= "Variáveis da CPU",
                     border_style= Style(color= "bright_cyan"))

def cpuVariables():
    if _cpuVariables._instance is None:
        _cpuVariables._instance = _cpuVariables()
    return _cpuVariables._instance