from tkinter import ttk
import DaCapoHandler

class DaCapo_View(ttk.Frame):
    
    def __init__(self, parent):
        super().__init__(parent)
        self.handler = DaCapoHandler.DaCapo_Handler(self)
        
        self.boton_musicXML = ttk.Button(self, text="Open MusicXML File", command=self.__select_musicxml_file)
        self.boton_musicXML.grid(row=0, column=0)
        
        self.label_DaCapo = ttk.Label(self, text='DaCapo Sheet Viewer')
        self.label_DaCapo.grid(row=0, column=1) 
        
        self.boton_mp3 = ttk.Button(self, text="Open MP3 File", command=self.__select_mp3_file)
        self.boton_mp3.grid(row=0, column=2)
        
        self.label_prototype = ttk.Label(self, text='The current version is a prototype. Many functions are yet to be implemented. As of now the app can only function with songs played at a 120 bpm and musicXML files that have a set 120 bpm.')
        self.label_prototype.grid(row=1, column=0, columnspan=3)    
    
    
    
    
    # Function to select a MusicXML file
    def __select_musicxml_file(self):
        file_path = ttk.filedialog.askopenfilename(
            title="Select a MusicXML file",
            filetypes=(("MusicXML files", "*.mxl"), ("All files", "*.*"))
        )
        if file_path:
            self.handler.retrieve_musicXML_file(file_path)
        else:
            ttk.messagebox.showinfo("Alert", "No se ha seleccionado un archivo!")
    
    # Function to select a MP3 file
    def __select_mp3_file(self):
        file_path = ttk.filedialog.askopenfilename(
            title="Select a MP3 file",
            filetypes=(("MP3 files", "*.mp3"), ("All files", "*.*"))
        )
        if file_path:
            self.handler.retrieve_mp3_file(file_path)
        else:
            ttk.messagebox.showinfo("Alert", "No se ha seleccionado un archivo!")
        
    # Function to display an image
    def display_image(self, image):
        pass
        