from music21 import *
from tkinter import filedialog


def color_numbered_measure(score, measure_number, color ='red', color_default = 'black'):    
    # Iterate through all elements on the selected measure
    for element in score.parts[0].measures(measure_number, measure_number).flat:
        if isinstance(element, note.Note) or isinstance(element, chord.Chord):
            element.style.color = color
            
    for element in score.parts[0].measures(measure_number+1, measure_number+1).flat:
        if isinstance(element, note.Note) or isinstance(element, chord.Chord):
            element.style.color = color_default
    # Show or save the modified score
    image = score.show('lily.pdf')  # Display the modified score

    return score

def test_score_highlight(score_path):
    score = converter.parse(score_path)
    color_numbered_measure(score,3)    





score_path = filedialog.askopenfilename(
    title="Select a MusicXML file",
    filetypes=(("MusicXML files", "*.mxl"), ("All files", "*.*"))
)

test_score_highlight(score_path)