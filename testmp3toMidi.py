import librosa
from tkinter import filedialog

from sound_to_midi.monophonic import wave_to_midi

input_path = filedialog.askopenfilename(
    title="Select a MusicXML file",
    filetypes=(("Mp3 files", "*.mp3"), ("All files", "*.*"))
)

print("Starting...")
file_in = input_path
file_out = "./testMidi3.mid"
y, sr = librosa.load(file_in, sr=None)
print("Audio file loaded!")
midi = wave_to_midi(y, sr)
print("Conversion finished!")
with open (file_out, 'wb') as f:
    midi.writeFile(f)
print("Done. Exiting!")