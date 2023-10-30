import pygame
from tkinter import filedialog
import time

def play_mp3_file(mp3_path):
    try:
        pygame.mixer.init()
        pygame.mixer.music.load(mp3_path)
        pygame.mixer.music.play()
        pygame.mixer.music.set_volume(1.0)  # You can adjust the volume (0.0 to 1.0)
    except Exception as e:
        print(f"An error occurred: {str(e)}")

# Example usage:
mp3_file_path = filedialog.askopenfilename(
    title="Select a MP3 file",
    filetypes=(("MP3 files", "*.mp3"), ("All files", "*.*"))
)

play_mp3_file(mp3_file_path)

print("sigue corriendo")
time.sleep(10)
print("sigue corriendo despues de 10 seg")
time.sleep(1)
print("siguio corriendo, fin del test")
while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)