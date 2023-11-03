from tkinter import ttk, Toplevel
import tkinter as tk
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
        logo_image = logo_image.resize(size=(200, 65))

        # Convert the PIL image to a Tkinter PhotoImage
        logo = ImageTk.PhotoImage(logo_image)
        self.logo = ttk.Label(self, image=logo)
        self.logo.image = logo #Prevents the image from being garbage collected
        self.logo.grid(row=0, column=1) 
        
        self.boton_mp3 = ttk.Button(self, text="Open MP3 File", command=self.__select_mp3_file)
        self.boton_mp3.grid(row=0, column=2)
        
        self.label_prototype = ttk.Label(self, text='The current version is a prototype.As of now the app only functions if the MusicXML file and the mp3 file have the same bpm.')
        self.label_prototype.grid(row=1, column=0, columnspan=3)    
        
        self.boton_tutorial = ttk.Button(self, text="Mostrar Tutorial", command=self.__mostrar_tutorial)
        self.boton_tutorial.grid(row=2, column=0, columnspan=3)
        
        self.boton_reproducir = ttk.Button(self, text="Reproducir Audio", command=self.__play_mp3_file)
        self.boton_reproducir.grid(row=3, column=0, columnspan=3)   
    
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
        self.handler.start_playing_mp3_file()
    
    def __mostrar_tutorial(self):
        # Create a new window
        tutorial_window = Toplevel()
        tutorial_window.title("Tutorial Window")

        # Create a text widget to display the long message
        text_widget = tk.Text(tutorial_window, wrap=tk.WORD)
        text_widget.pack()

        # Add the long message as a paragraph
        long_message = """
        Bienvenido al prototipo de DaCapo - Music Sheet Viewer.
        
        Para utilizar la aplicación, es importante realizar los siguientes pasos en el orden establecido:
        
        1. Cargar el archivo MusicXML de la partitura que se desea mostrar.
        2. Cargar el archivo MP3 de la misma partitura (Se debe hacer siempre despues de subir el archivo MusicXML)
        3. Presionar el boton de reproducir audio.
        
        Si durante el uso de la aplicación se desea probar con otra partitura, hará falta empezar desde el punto 1. Si desea solamente sustituir el audio, basta con empezar desde el punto 2. Siempre debe subir la partitura primero al archivo MP3.
        """

        text_widget.insert(tk.END, long_message)

        # Make the text widget read-only
        text_widget.config(state=tk.DISABLED)

        # Create a scrollbar for the text widget
        scrollbar = tk.Scrollbar(tutorial_window, command=text_widget.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        text_widget.config(yscrollcommand=scrollbar.set)
        tutorial_window.update()
    
    # Function to display an image
    def display_image(self, image):
        if hasattr(self, "image"):
            self.image.image = None
            self.image = None
        self.image = ttk.Label(self, image=image)
        self.image.grid(row=4, column=0, columnspan=3)
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
        
    def error_message(self, message):
        messagebox.showerror("Error", "The following error has ocurred: " + str(message))
        
    def info_message(self, message):
        messagebox.showinfo("Info", message)