import tkinter as tk
from DaCapoView import DaCapo_View

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        # Set the root window size to match the screen
        self.geometry(f"{screen_width}x{screen_height}")
        
        self.title('DaCapo Demo')
        
        view = DaCapo_View(self)
        view.grid(row=0, column=0)
        