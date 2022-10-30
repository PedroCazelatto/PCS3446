import os

from rich.align import Align
from rich.style import Style
from rich.panel import Panel
from rich.console import RenderableType
from rich.tree import Tree

from textual.reactive import Reactive
from textual.widget import Widget

import os

class _virtualDisc(Widget):
    _instance = None
    
    # def createFile(self, fileName: str):
    #     if os.path.exists("./root/" + fileName):
    #         return False
    #     with open("./root/" + fileName):
    #         pass
    
    def deleteFile(self, fileName: str) -> bool:
        if fileName[:6] == "loader":
            return False
        if os.path.exists("./root/" + fileName):
            os.remove("./root/" + fileName)
            return True
        return False

    def render(self) -> RenderableType:
        archives = Tree("root")
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