from rich.style import Style
from rich.panel import Panel
from rich.layout import Layout
from rich.console import RenderableType

from textual.widget import Widget

import pyLib.memory
import pyLib.virtualDisc
import pyLib.processAdmin
import pyLib.cpuVariables

class _interface(Widget):
    _instance = None
        
    def render(self) -> RenderableType:
        pyLib.cpuVariables.cpuVariables().refresh()
        pyLib.virtualDisc.virtualDisc().refresh()
        pyLib.memory.memory().refresh()
        pyLib.processAdmin.processAdmin().refresh()
        layout = Layout()
        layout.split_row(
            Layout(pyLib.virtualDisc.virtualDisc(), ratio= 7),
            Layout(pyLib.memory.memory(), ratio= 7),
            Layout(pyLib.cpuVariables.cpuVariables(), ratio= 7),
            Layout(pyLib.processAdmin.processAdmin(), ratio= 9)
        )
        return Panel(layout,
                     border_style= Style(color= "yellow1"))

def interface():
    if _interface._instance is None:
        _interface._instance = _interface()
    return _interface._instance