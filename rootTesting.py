import tkinter as tk
from tkinter import filedialog
from music21 import converter, environment
from PIL import ImageTk, Image

# Set the path to your Lilypond installation
environment.set("lilypondPath", "C:/Program Files (x86)/LilyPond/usr/bin/lilypond.exe")

# Create a Tkinter window
root = tk.Tk()
root.title("MusicXML Viewer")

# Function to convert MusicXML to an image and display it
def display_music_sheet(file_path):
    # Convert MusicXML to an image (PNG)
    output_image_path = "./MusicSheet/music_sheet"
    score = converter.parse(file_path)
    score.write('lily.png', output_image_path)
    
    # Load the image using Tkinter
    display_image(output_image_path + ".png")

# Function to display an image
def display_image(image_path):
    # Open the image using PIL
    pil_image = Image.open(image_path)

    # Convert the PIL image to a Tkinter PhotoImage
    img = ImageTk.PhotoImage(pil_image)

    # Create a label to display the image
    panel = tk.Label(root, image=img)
    panel.pack(side="bottom", fill="both", expand="yes")

    # Keep a reference to the image to prevent it from being garbage-collected
    panel.image = img

# Function to select a MusicXML file and trigger display
def select_musicxml_file():
    file_path = filedialog.askopenfilename(
        title="Select a MusicXML file",
        filetypes=(("MusicXML files", "*.mxl"), ("All files", "*.*"))
    )
    if file_path:
        display_music_sheet(file_path)

# Create a button to trigger the file dialog
button = tk.Button(root, text="Open MusicXML File", command=select_musicxml_file)
button.pack(padx=20, pady=20)

# Start the Tkinter main loop
root.mainloop()