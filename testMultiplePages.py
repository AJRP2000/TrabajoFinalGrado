from tkinter import filedialog
import music21
import math

def divide_musicxml_in_pages(input_path, measures_per_page = 20):
    # Load the MusicXML file
    score = music21.converter.parse(input_path)
    
    # Split the score into pages
    parts = score.getElementsByClass('Part')
    page_count = math.ceil(len(parts[0].getElementsByClass('Measure')) / measures_per_page)
    
    score_pages = []

    for page_num in range(page_count):
        # Create a new stream for the current page
        page_score = music21.stream.Score()

        # Add measures to the page
        for part in parts:
            measures = part.getElementsByClass('Measure')[page_num * measures_per_page:(page_num + 1) * measures_per_page]
            page_score.append(measures)

        # Generate a filename for the page
        #output_file = os.path.join(output_dir, f'page_{page_num + 1}.mxl')

        # Save the page as a separate MusicXML file
        #page_score.write('musicxml', output_file)
        
        score_pages.append(page_score)

    return score_pages

def _test_multiple_pages(input_path):
    score_pages = divide_musicxml_in_pages(input_path, 5)
    print(len(score_pages))
    score_pages[0].show()


input_path = filedialog.askopenfilename(
    title="Select a MusicXML file",
    filetypes=(("MusicXML files", "*.mxl"), ("All files", "*.*"))
)
_test_multiple_pages(input_path)