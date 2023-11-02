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
        
        if current_tick >= ticks_per_measure:
            output_midi_track = current_track
            output_tracks.append(output_midi_track)
            current_tick = 0
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

def compare_notes_between_two_arrays(array_being_compared, array_to_be_compared_to, error_margin, similarity_percentage_required):
        hits = 0
        if(len(array_being_compared)> len(array_to_be_compared_to)):
            maximum = len(array_to_be_compared_to)
            for value1 in array_to_be_compared_to:
                for value2 in array_being_compared:
                    if abs(value1 - value2) <= error_margin:
                        hits += 1
                        break
        else:
            maximum = len(array_being_compared)
            for value1 in array_being_compared:
                for value2 in array_to_be_compared_to:
                    if abs(value1 - value2) <= error_margin:
                        hits += 1
                        break
                
        if(maximum <= 0):
            return True
            
        percentage_of_hits = hits/maximum
        if(percentage_of_hits >= similarity_percentage_required):
            return True
        
        return False

def safe_list_access(my_list, outer_index, inner_index):
    if 0 <= outer_index < len(my_list):
        inner_list = my_list[outer_index]
        if 0 <= inner_index < len(inner_list):
            # Both indices are within the valid range
            return True
    
    return False

if __name__ == "__main__":
    input_midi_path = "./midiFiles/midiPartitura.mid"  
    music_sheet_midi_splits=split_midi_by_duration(input_midi_path, duration=4, measures_per_page=15)
    input_midi_path2 = "./midiFiles/midiAudio.mid"
    mp3_midi_splits=split_midi_by_duration(input_midi_path2, duration=4, measures_per_page=15)
    print("done splitting")
    
    current_page = 0
    current_measure = 1
    error_margin = 9
    percentage_required = 0.5
    
    #Testing Algorithm of comparison
    while (safe_list_access(music_sheet_midi_splits, current_page, current_measure) and safe_list_access(mp3_midi_splits, current_page, current_measure)): 
        current_measure_mp3 = mp3_midi_splits[current_page][current_measure-1]
        current_measure_music_sheet = music_sheet_midi_splits[current_page][current_measure-1]
        if not compare_notes_between_two_arrays(current_measure_mp3, current_measure_music_sheet, error_margin, percentage_required):
            print("Error en el compas" + str(current_measure) + " pagina " + str(current_page))
            break
            
        if(current_measure >= 15):
            current_measure = 1
            current_page += 1
        else:
            current_measure += 1
            
            
    print("finished comparing")