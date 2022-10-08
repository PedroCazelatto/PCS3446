from rich.style import Style
from rich.panel import Panel
from rich.layout import Layout
from rich.console import RenderableType

from textual.widget import Widget

from pyLib.memory import memory
from pyLib.virtualDisc import virtualDisc
from pyLib.processAdmin import processAdmin

class _interface(Widget):
    _instance = None
        
    def render(self) -> RenderableType:
        virtualDisc().refresh()
        memory().refresh()
        processAdmin().refresh()
        layout = Layout()
        layout.split_row(
            Layout(virtualDisc()),
            Layout(memory()),
            Layout(processAdmin())
        )
        return Panel(layout,
                     border_style= Style(color= "yellow1"))

def interface():
    if _interface._instance is None:
        _interface._instance = _interface()
    return _interface._instance