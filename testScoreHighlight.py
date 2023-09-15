from music21 import *

def color_numbered_measure(score, measure_number, color ='red'):
    # Convert the input score to a Stream object
    score = converter.parse(score)
    
    # Iterate through all elements on the selected measure
    for element in score.parts[0].measures(measure_number, measure_number).flat:
        if isinstance(element, note.Note) or isinstance(element, chord.Chord):
            element.style.color = color
    
    # Show or save the modified score
    score.show()  # Display the modified score

score_path = 'C:/Users/anton/OneDrive/Escritorio/Twinkle star files/Twinle Star ORIGINAL MUSESCORE MUSICXML.mxl'
color_numbered_measure(score_path,3)