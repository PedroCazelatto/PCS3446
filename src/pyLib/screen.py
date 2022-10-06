from rich.layout import Layout

from textual.app import App
from textual.reactive import Reactive
from textual.widgets import Footer, Header

# from initialScreen import patinhOs
# from memoryApps import memoryApps
# from virtualDisc import virtualDisc
from pyLib.helpList import helpList
from pyLib.cmdLine import cmdLine
from pyLib.interface import interface

class screen(App):
    show_help = Reactive(False)
    
    async def on_load(self):
        await self.bind("ctrl+a", "toggle_help", "Ajuda  ")
        await self.bind("ctrl+c", "quit", "Saída  ")
    
    def watch_show_help(self, show_help: bool):
        self.barra.animate("layout_offset_x", 0 if show_help else 40)
        
    def action_toggle_help(self):
        self.show_help = not self.show_help
    
    # O que acontece ao rodar o programa (SETUP)
    async def on_mount(self):
        
        header = Header(tall=False) # Cria o cabecalho
        await self.view.dock(header) # Adiciona o cabecalho no topo
                
        footer = Footer()
        await self.view.dock(footer, edge="bottom") # Adiciona o rodape

        self.barra = helpList() # Cria uma barra
        await self.view.dock(self.barra, edge="right", size=40, z=1)
        
        self.barra.layout_offset_x = 40

        homeGrid = await self.view.dock_grid()
        
        homeGrid.add_row("row1", fraction= 3)
        homeGrid.add_row("row2", fraction= 1, max_size= 13, min_size= 3)
        homeGrid.add_column("col")
        homeGrid.place(interface(), cmdLine())