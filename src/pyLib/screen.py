from rich.layout import Layout

from textual.app import App
from textual.reactive import Reactive
from textual.widgets import Footer, Header

import pyLib.helpList
import pyLib.cmdLine
import pyLib.interface
import pyLib.memory

class screen(App):
    show_help = Reactive(False)
    helpBarSize = 50
    
    async def on_load(self):
        await self.bind("ctrl+a", "toggle_help", "Ajuda  ")
        await self.bind("ctrl+c", "quit", "Saída  ")
    
    def watch_show_help(self, show_help: bool):
        self.helpBar.animate("layout_offset_x", 0 if show_help else self.helpBarSize)
        
    def action_toggle_help(self):
        self.show_help = not self.show_help
    
    # O que acontece ao rodar o programa (SETUP)
    async def on_mount(self):
        
        header = Header(tall=False)
        await self.view.dock(header)
                
        footer = Footer()
        await self.view.dock(footer, edge="bottom")

        self.helpBar = pyLib.helpList.helpList()
        await self.view.dock(self.helpBar, edge= "right", size= self.helpBarSize, z= 1)
        
        self.helpBar.layout_offset_x = self.helpBarSize

        homeGrid = await self.view.dock_grid()
        
        homeGrid.add_row("row1")
        homeGrid.add_row("row2", size= 12)
        homeGrid.add_column("col")
        homeGrid.place(pyLib.interface.interface(), pyLib.cmdLine.cmdLine())
        
        pyLib.memory.memory().loadLoader()