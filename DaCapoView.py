from tkinter import ttk, Toplevel
from tkinter import filedialog, messagebox
import DaCapoHandler
from PIL import ImageTk, Image

class DaCapo_View(ttk.Frame):
    
    def __init__(self, parent):
        super().__init__(parent)
        self.handler = DaCapoHandler.DaCapo_Handler(self)
        
        self.boton_musicXML = ttk.Button(self, text="Open MusicXML File", command=self.__select_musicxml_file)
        self.boton_musicXML.grid(row=0, column=0)
        
        logo_image = Image.open("DaCapoLogo.png")
        logo_image = logo_image.resize(size=(400, 130))

        # Convert the PIL image to a Tkinter PhotoImage
        logo = ImageTk.PhotoImage(logo_image)
        self.logo = ttk.Label(self, image=logo)
        self.logo.image = logo #Prevents the image from being garbage collected
        self.logo.grid(row=0, column=1) 
        
        self.boton_mp3 = ttk.Button(self, text="Open MP3 File", command=self.__select_mp3_file)
        self.boton_mp3.grid(row=0, column=2)
        
        self.label_prototype = ttk.Label(self, text='The current version is a prototype. Many functions are yet to be implemented. As of now the app can only function with songs played at a 120 bpm and musicXML files that have a set 120 bpm.')
        self.label_prototype.grid(row=1, column=0, columnspan=3)    
        
        self.boton_reproducir = ttk.Button(self, text="Reproducir Audio", command=self.__play_mp3_file)
        self.boton_reproducir.grid(row=2, column=0, columnspan=3)   
    
    
    
    # Function to select a MusicXML file
    def __select_musicxml_file(self):
        file_path = filedialog.askopenfilename(
            title="Select a MusicXML file",
            filetypes=(("MusicXML files", "*.mxl"), ("All files", "*.*"))
        )
        if file_path:
            self.handler.retrieve_musicXML_file(file_path)
        else:
            messagebox.showinfo("Alert", "No se ha seleccionado un archivo!")
    
    # Function to select a MP3 file
    def __select_mp3_file(self):
        file_path = filedialog.askopenfilename(
            title="Select a MP3 file",
            filetypes=(("MP3 files", "*.mp3"), ("All files", "*.*"))
        )
        if file_path:
            self.handler.retrieve_mp3_file(file_path)
        else:
            messagebox.showinfo("Alert", "No se ha seleccionado un archivo!")
        
    #Function to play the MP3 File
    def __play_mp3_file(self):
        pass
    
    # Function to display an image
    def display_image(self, image):
        self.image = ttk.Label(self, image=image)
        self.image.grid(row=3, column=0, columnspan=3)
        self.image.image = image #Prevents the image from being garbage collected
        self.update()
        
        
    def create_loading_window(self, texto):
        self.loading_window = Toplevel(self)
        self.loading_window.title("Cargando...")
        self.loading_window.label = ttk.Label(self.loading_window, text=texto, font=("Helvetica", 18))
        self.loading_window.label.grid(row=0, column=0)
        self.update()
    
    def delete_loading_window(self):
        self.loading_window.destroy()
        self.loading_window = None