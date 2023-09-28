from tkinter import ttk
import DaCapoHandler

class DaCapo_View(ttk.Frame):
    
    def __init__(self, parent):
        super().__init__(parent)
        self.handler = DaCapoHandler.DaCapo_Handler(self)
    
        
        
        