from mido import MidiFile

def split_midi_by_duration(input_midi_path, duration, measures_per_page):
    try:
        midi_file = MidiFile(input_midi_path)
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

if __name__ == "__main__":
    input_midi_path = "./midiFiles/midiPartitura.mid"  # Replace with your input MIDI file path
    split_midi_by_duration(input_midi_path, duration=2.727272727272727, measures_per_page=30)