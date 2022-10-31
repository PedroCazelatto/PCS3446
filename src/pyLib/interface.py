from rich.style import Style
from rich.panel import Panel
from rich.layout import Layout
from rich.console import RenderableType

from textual.widget import Widget

import pyLib.memory
import pyLib.virtualDisc
import pyLib.processAdmin

class _interface(Widget):
    _instance = None
        
    def render(self) -> RenderableType:
        pyLib.virtualDisc.virtualDisc().refresh()
        pyLib.memory.memory().refresh()
        pyLib.processAdmin.processAdmin().refresh()
        layout = Layout()
        layout.split_row(
            Layout(pyLib.virtualDisc.virtualDisc()),
            Layout(pyLib.memory.memory()),
            Layout(pyLib.processAdmin.processAdmin())
        )
        return Panel(layout,
                     border_style= Style(color= "yellow1"))

def interface():
    if _interface._instance is None:
        _interface._instance = _interface()
    return _interface._instance