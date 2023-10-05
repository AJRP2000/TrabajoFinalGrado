import subprocess
import tempfile
import os
from music21 import converter

def generate_score_image(score, output_image_path):
    try:
        # Create a temporary LilyPond file
        lilypond_code = score.lily()
        temp_lilypond_file = tempfile.NamedTemporaryFile(delete=False, suffix=".ly")
        with open(temp_lilypond_file.name, "w") as f:
            f.write(lilypond_code)
        
        # Generate the image using LilyPond
        subprocess.run(["lilypond", "-o", os.path.dirname(output_image_path), temp_lilypond_file.name])
        
        # Rename the LilyPond-generated image to the desired output path
        lilypond_image = os.path.splitext(temp_lilypond_file.name)[0] + ".png"
        os.rename(lilypond_image, output_image_path)
    except Exception as e:
        print("Error:", e)

# Example usage:
if __name__ == "__main__":
    # Load a Music21 score (replace with your own score loading logic)
    score = converter.parse('C:/Users/anton/OneDrive/Escritorio/Twinkle star files/Twinle Star ORIGINAL MUSESCORE MUSICXML.mxl')
    
    # Specify the output image path
    output_image_path = "testPages/output_score.png"
    
    # Generate the image from the score
    generate_score_image(score, output_image_path)