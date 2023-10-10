from music21 import *
from PIL import Image
import os
import glob

def delete_files_except_png(folder_path):
    try:
        # Get a list of all files in the directory
        all_files = glob.glob(os.path.join(folder_path, '*'))

        # Iterate through the files and delete those that don't end with '.png'
        for file_path in all_files:
            if not file_path.endswith('.png'):
                os.remove(file_path)
                print(f"Deleted: {file_path}")

        print("Deletion completed successfully.")

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        
        
# Replace 'path_to_your_score.musicxml' with the path to your actual MusicXML file
input_file = 'C:/Users/anton/OneDrive/Escritorio/Twinkle star files/Twinle Star ORIGINAL MUSESCORE MUSICXML.mxl'

# Parse the MusicXML file
score = converter.parse(input_file)

# Specify the output PDF file
pdf_output_file = './Views/page'

# Use LilyPond to create a PDF
score.write('lily.png', pdf_output_file + '1')

score.write('lily.png', pdf_output_file+'2')

delete_files_except_png('./Views/')
