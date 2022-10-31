from rich.align import Align
from rich.style import Style
from rich.panel import Panel
from rich.console import RenderableType
from rich.tree import Tree

from textual.widget import Widget

from pyLib.infoLists import validCommands, helpContents

class helpList(Widget):
    
    helpBar = Tree("Comandos")
    
    for idx, seq in enumerate(validCommands):
        helpBar.add(seq.capitalize()).add(helpContents[idx])
    
    def render(self) -> RenderableType:
        return Panel(self.helpBar,
                     title= "Comandos",
                     border_style= Style(color= "bright_magenta"))
