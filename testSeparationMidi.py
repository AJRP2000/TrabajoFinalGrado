from mido import MidiFile

def split_midi_by_duration(input_midi_path, duration, measures_per_page):
    try:
        midi_file = MidiFile(input_midi_path)
    except FileNotFoundError:
        print("MIDI file not found.")
        return

    current_time = 0
    current_track = []
    output_tracks = []
    for i, msg in enumerate(midi_file.play()):
        current_time += msg.time
        if(msg.type == 'note_on'):
            current_track.append(msg)

        if current_time >= duration:
            output_midi_track = current_track
            output_tracks.append(output_midi_track)
            current_time = 0
            current_track = []


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

if __name__ == "__main__":
    input_midi_path = "./midiFiles/midiPartitura.mid"  # Replace with your input MIDI file path
    split_midi_by_duration(input_midi_path, duration=3, measures_per_page=30)