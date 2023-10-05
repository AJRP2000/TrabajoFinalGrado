import music21
import math
from PIL import ImageTk, Image


class DaCapo_Handler:
    def __init__(self, view):
        self.dacapo_view = view
    
    #(display_music_sheet)
    # Function to receive the path to a MusicXML file, save it as a Score and trigger display.
    def retrieve_musicXML_file(self, file_path):
        self.score = music21.converter.parse(file_path)
        measures_per_page = 20
        self.score_pages = self.__divide_musicxml_in_pages(self.score, measures_per_page)
        
    
        # Load the image using Tkinter
        image = self.__create_image(self.score_pages[0])
        self.dacapo_view.display_image(image)
    
    def retrieve_mp3_file(self, file_path):
        pass
    
    #Receives a score and divides it into pages based on th
    def __divide_musicxml_in_pages(score, measures_per_page = 20):
        
        # Split the score into pages
        parts = score.getElementsByClass('Part')
        page_count = math.ceil(len(parts[0].getElementsByClass('Measure')) / measures_per_page)
        
        score_pages = []

        for page_num in range(page_count):
            # Create a new stream for the current page
            page_score = music21.stream.Stream()

            # Add measures to the page
            for part in parts:
                measures = part.getElementsByClass('Measure')[page_num * measures_per_page:(page_num + 1) * measures_per_page]
                page_score.append(measures)
            
            score_pages.append(page_score)

        return score_pages
    
    #Receives a score and creates an image of said score
    def __create_image(self, score):
        pass