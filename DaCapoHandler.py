from music21 import *
import music21
import math
import os
import glob
from PIL import ImageTk, Image
import librosa
from sound_to_midi.monophonic import wave_to_midi
import time
import pygame
import mido


class DaCapo_Handler:
    def __init__(self, view):
        self.dacapo_view = view
    
    #(display_music_sheet)
    # Function to receive the path to a MusicXML file, save it as a Score and trigger display.
    def retrieve_musicXML_file(self, file_path):
        self.dacapo_view.create_loading_window("Cargando Archivo...")
        self.score = music21.converter.parse(file_path)
        
        self.dacapo_view.delete_loading_window()
        self.dacapo_view.create_loading_window("Procesando Archivo...")
        
        self.music_sheet_midi_path = "./midiFiles/midiPartitura.mid"
        self.__write_score_to_midi(self.score, self.music_sheet_midi_path)
        
        #We select the amount of measures to be shown per page
        self.measures_per_page = 30
        
        self.music_sheet_midi_splits = self.__split_midi_by_duration(self.music_sheet_midi_path, self.measure_seconds, self.measures_per_page)
        
        self.dacapo_view.delete_loading_window()
        self.dacapo_view.create_loading_window("Creando Imagenes de la Partitura...")
        
        self.score_pages = self.__divide_musicxml_in_pages(self.score, self.measures_per_page)
        self.score_pages_paths = self.__create_png_list_scores(self.score_pages, self.measures_per_page)    
    
        # Load the image using Tkinter
        image = self.__create_image(self.score_pages_paths[0][0])
        
        self.dacapo_view.delete_loading_window()
        self.dacapo_view.display_image(image)
    
    def retrieve_mp3_file(self, file_path):
        if not (self.music_sheet_midi_path):
            self.dacapo_view.error_message("No se ha cargado una partitura aun.")
            return 0

        self.dacapo_view.create_loading_window("Cargando Archivo Mp3...")
        file_in = file_path
        file_out = "./midiFiles/midiAudio.mid"
        y, sr = librosa.load(file_in, sr=None)
        print("Archivo MP3 Cargado")
        
        self.dacapo_view.delete_loading_window()
        self.dacapo_view.create_loading_window("Convirtiendo archivo MP3...")
        
        midi = wave_to_midi(y, sr)
        print("Conversion Terminada")
        with open (file_out, 'wb') as f:
            midi.writeFile(f)
            
        print("Archivo Guardado")
        self.dacapo_view.delete_loading_window()
        self.dacapo_view.create_loading_window("Procesando archivo...")
        
        mp3_midi_splits = self.__split_midi_by_duration(file_out ,self.measure_seconds, self.measures_per_page)
        self.mp3_midi_splits = mp3_midi_splits
        
        self.mp3_path = file_path
        self.midi_mp3_path = file_out
        self.dacapo_view.delete_loading_window()
        self.dacapo_view.info_message("El archivo ha sido cargado con exito!")
    
    def start_playing_mp3_file(self):
        
        if not self.mp3_midi_splits and not self.music_sheet_midi_splits:
            self.dacapo_view.error_message("Primero debe cargar la partitura y el archivo mp3.")
            return 0
            
        
        self.__play_mp3_file(self.mp3_path)
        
        while (pygame.mixer.music.get_busy() and True ): #Falta medir si quedan compases en ambos midis
            pygame.time.Clock().tick(10)
    
    def __play_mp3_file(self, mp3_path):
        pygame.mixer.init()
        pygame.mixer.music.load(mp3_path)
        pygame.mixer.music.set_volume(1.0)
        pygame.mixer.music.play()
    
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
    
    def __write_score_to_midi(self, score, output_filename):
        # Write the MIDI file
        score.write('midi', output_filename)
        
        #Sets the default BPM to be 120
        self.score_bpm = 120
        
        # Extract time signature information
        time_signatures = None
        
        for element in score.flat:
            if isinstance(element, tempo.MetronomeMark):
                #Sets bpm to be the one written in the score
                self.score_bpm  = element.number
            if 'TimeSignature' in element.classes:
                #Sets the time signature of the song
                time_signatures = ({
                    "numerator": element.numerator,
                    "denominator": element.denominator
                })
        
        if not time_signatures:
            self.measure_seconds = 60.0 / self.score_bpm * 4 #Default measure seconds is set to 4 beats per measure
        else:
            #Sets the measure seconds according to the BPM and the time signature given by the musicxml file
            self.measure_seconds = 60.0 / self.score_bpm * (time_signatures['numerator'] / time_signatures['denominator']) * time_signatures['numerator']

        self.midi_partitura_path = output_filename
    
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
        
        
    def split_midi_by_duration(input_midi_path, duration, measures_per_page):
        try:
            midi_file = mido.MidiFile(input_midi_path)
        except FileNotFoundError:
            print("MIDI file not found.")
            return

        ticks_per_beat = midi_file.ticks_per_beat
        ticks_per_measure = int(ticks_per_beat * duration)

        current_tick = 0
        current_track = []
        output_tracks = []
        for msg in midi_file.tracks[1]:
            current_tick += msg.time
            
            if current_tick >= duration:
                output_midi_track = current_track
                output_tracks.append(output_midi_track)
                current_tick = current_tick - ticks_per_measure
                current_track = []
                
            if(msg.type == 'note_on'):
                current_track.append(msg.note)


        result = []
        current_subarray = []

        for element in output_tracks:
            current_subarray.append(element)

            if len(current_subarray) == measures_per_page:
                result.append(current_subarray)
                current_subarray = []

        if current_subarray:
            result.append(current_subarray)

        return result