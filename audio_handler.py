import numpy as np
import sounddevice as sd
import threading
from frequencies import note_frequencies

# Shared settings for current tone
current_tone_settings = {'frequency': 440, 'amplitude': 0.5, 'current_note': 'A'}
current_tone_thread = None
loop = False
stop_requested = False

def generate_tone(frequency, amplitude, duration=1.0):
    sample_rate = 44100
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
    wave = amplitude * np.sin(2 * np.pi * frequency * t)
    return wave.astype(np.float32), sample_rate

def play_tone():
    global current_tone_thread, stop_requested
    stop_requested = False
    if current_tone_thread and current_tone_thread.is_alive():
        return  # Avoid starting a new thread if already playing
    thread_target = lambda: audio_stream(current_tone_settings['frequency'], current_tone_settings['amplitude'])
    current_tone_thread = threading.Thread(target=thread_target)
    current_tone_thread.start()

def audio_stream(frequency, amplitude):
    wave, sample_rate = generate_tone(frequency, amplitude)
    stream = sd.OutputStream(samplerate=sample_rate, channels=1, dtype='float32')
    stream.start()
    try:
        while not stop_requested:
            stream.write(wave)
            if not loop:
                break
            # Check if tone settings have changed
            frequency, amplitude = current_tone_settings['frequency'], current_tone_settings['amplitude']
            wave, _ = generate_tone(frequency, amplitude)
    finally:
        stream.stop()

def stop_playback():
    global stop_requested
    stop_requested = True
    if current_tone_thread:
        current_tone_thread.join()

def toggle_loop(state):
    global loop
    loop = state

def set_current_note(note):
    current_tone_settings['current_note'] = note
    current_tone_settings['frequency'] = note_frequencies[note]

def set_frequency(freq):
    current_tone_settings['frequency'] = freq

def set_amplitude(amp):
    current_tone_settings['amplitude'] = amp
