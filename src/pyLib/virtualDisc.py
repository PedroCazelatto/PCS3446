import os

from rich.tree import Tree
from rich.text import Text
from rich.style import Style
from rich.panel import Panel
from rich.console import RenderableType

from textual.widget import Widget

class _virtualDisc(Widget):
    _instance = None
    
    def createFile(self, fileName: str):
        if os.path.exists("./root/" + fileName):
            return [False, "Arquivo já existe"]
        with open("./root/" + fileName, 'w'):
            pass
        return [True, "Arquivo " + fileName + " criado"]
    
    def deleteFile(self, fileName: str):
        os.remove("./root/" + fileName)
        return [True, "Arquivo " + fileName + " apagado"]

    def render(self) -> RenderableType:
        archives = Tree(Text("root", style= Style(bold= True)))
        for arch in os.scandir("./root"):
            if arch.is_file():
                if arch.name[:6] ==  "loader":
                    continue
                archives.add(arch.name)
        return Panel(archives,
                     title="Disco (Pasta externa)",
                     border_style= Style(color= "bright_cyan"))

def virtualDisc():
    if _virtualDisc._instance is None:
        _virtualDisc._instance = _virtualDisc()
    return _virtualDisc._instance