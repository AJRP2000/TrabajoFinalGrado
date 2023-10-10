from music21 import *
import music21
import math
import os
import glob
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
        self.score_pages_paths = self.__create_png_list_scores(self.score_pages, measures_per_page)    
    
        # Load the image using Tkinter
        image = self.__create_image(self.score_pages_paths[0][0])
        self.dacapo_view.display_image(image)
    
    def retrieve_mp3_file(self, file_path):
        pass
    
    #Function that receives a list of score pages and creates 
    def __create_png_list_scores(self, score_pages, measures_per_page):
        self.__delete_all_files('./ImagePages/')
        
        score_pages_paths = []
        for page_number in range(len(score_pages)) :
            path_page = "./ImagePages/page"+ str(page_number) + "measure"
            score_pages_paths.append(self.__create_colored_pngs(score_pages[page_number], measures_per_page, path_page))
        
        self.__delete_files_except_png('./ImagePages/')
        return score_pages_paths        
        
    def __create_colored_pngs(self, page, measures_per_page, path_page):
        page_paths = []
        for current_measure in range(len(page.elements)+1):
            if(current_measure== 0):
                score = page
            else:
                score = self.__color_numbered_measure(page, current_measure-1)
            path = path_page + str(current_measure)
            score.write('lily.png', path)
            page_paths.append(path + ".png")
        return  page_paths
        
    def __color_numbered_measure(self, score, measure_number, color ='red', color_default = 'black'):    
    # Iterate through all elements on the selected measure
        if(measure_number < len(score.elements)):
            #If it's not the first measure, recolor the previous measure to black
            if(measure_number > 0):
                for element in score.elements[measure_number-1]:
                    if isinstance(element, note.Note) or isinstance(element, chord.Chord):
                        element.style.color = color_default
            
            #Color current measure to red    
            for element in score.elements[measure_number]:
                if isinstance(element, note.Note) or isinstance(element, chord.Chord):
                    element.style.color = color
            
            #If it's not the last measure, make sure the next measure remains black 
            #(in lily.png format if a color is not specified, it will use the color of the previous note)
            if(measure_number+1 < len(score.elements)):        
                for element in score.elements[measure_number+1]:
                    if isinstance(element, note.Note) or isinstance(element, chord.Chord):
                        element.style.color = color_default

        return score
        
    
    #Receives a score and divides it into pages based on the measure number
    def __divide_musicxml_in_pages(self, score, measures_per_page = 20):
        
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
            
            score_pages.append(page_score)

        return score_pages
    
    #Deletes all files that aren't pngs in the ImagePages folder
    def __delete_files_except_png(self, folder_path):
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
    
    def __delete_all_files(self, folder_path):
        try:
            # Get a list of all files in the directory
            all_files = glob.glob(os.path.join(folder_path, '*'))

            # Iterate through the files and delete those that don't end with '.png'
            for file_path in all_files:
                os.remove(file_path)
                print(f"Deleted: {file_path}")

            print("Deletion completed successfully.")

        except Exception as e:
            print(f"An error occurred: {str(e)}")
    
    #Receives a path to the page and creates an image of said score
    def __create_image(self, path_to_image):
        # Open the image using PIL
        pil_image = Image.open(path_to_image)

        # Convert the PIL image to a Tkinter PhotoImage
        img = ImageTk.PhotoImage(pil_image)
        
        return img
        