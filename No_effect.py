import pyaudio
import numpy as np
from math import pi

def play(Note,single_note,note_length,volume):
    p = pyaudio.PyAudio()
    Fs = 16000
    frequncy = Note[single_note]
    stream = p.open(format=pyaudio.paFloat32,
                    channels=1,
                    rate=Fs,
                    output=True)
    #Play a sin-wave sound
    x = (np.sin(2*pi*np.arange(Fs*note_length)*frequncy/Fs)).astype(np.float32)
    #volume as 0%-100%
    output = volume/100*(x)
    stream.write(output)

    stream.stop_stream()
    stream.close()
    p.terminate()