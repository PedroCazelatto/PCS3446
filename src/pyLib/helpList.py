from rich.tree import Tree
from rich.text import Text
from rich.style import Style
from rich.panel import Panel
from rich.console import RenderableType

from textual.widget import Widget

from pyLib.infoLists import validCommands, helpContents

class helpList(Widget):
    
    helpBar = Tree(Text("Comandos", style= Style(bold= True)))
    
    for idx, seq in enumerate(validCommands):
        helpBar.add(Text(seq.capitalize(), style= Style(bold= True))).add(helpContents[idx])
    
    def render(self) -> RenderableType:
        return Panel(self.helpBar,
                     title= "Comandos",
                     border_style= Style(color= "bright_magenta"))
