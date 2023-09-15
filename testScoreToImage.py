from tkinter import filedialog
from music21 import *
import fitz  # PyMuPDF
from PIL import Image
from testScoreHighlight import color_first_measure_blue

# Replace 'path_to_your_score.musicxml' with the path to your actual MusicXML file
input_file = 'C:/Users/anton/OneDrive/Escritorio/Twinkle star files/Twinle Star ORIGINAL MUSESCORE MUSICXML.mxl'

# Parse the MusicXML file
s = converter.parse(input_file)

# Specify the output PDF file
pdf_output_file = './output'

# Use LilyPond to create a PDF
s.write('lily.pdf', pdf_output_file)

# Specify the output PNG file
png_output_file = './Views'

pdf_output_file = pdf_output_file + '.pdf'

pdf_document = fitz.open(pdf_output_file)

    # Select the first page (page 0)
page = pdf_document[0]

    # Get the dimensions of the page
page_rect = page.rect

    # Render the page as an image (300 DPI by default)
pix = page.get_pixmap(matrix=fitz.Matrix(300 / 72, 300 / 72))

    # Create a PIL image from the rendered pixmap
image = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)

    # Define the output file path
output_path = f"{png_output_file}/{pdf_output_file.split('/')[-1].replace('.pdf', '.png')}"

    # Save the PIL image as a PNG
image.save(output_path, "PNG")

    # Close the PDF file
pdf_document.close()