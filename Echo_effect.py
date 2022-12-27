import pyaudio

import wave
import struct

def clip16( x ):
    # Clipping for 16 bits
    if x > 32767:
        x = 32767
    elif x < -32768:
        x = -32768
    else:
        x = x
    return(x)

def play(single_note,volume):
    wavfile = 'Note'+str(single_note+1)+'.wav'
    # print('Play the wave file %s.' % wavfile)
    # Open the wave file
    wf = wave.open( wavfile, 'rb')
    # Set parameters of delay system
    # y(n) = b0 x(n) + G x(n-N)
    b0 = 1.0            # direct-path gain
    G = 0.8             # feed-forward gain
    delay_sec = 0.01    # delay in seconds, 50 milliseconds   Try delay_sec = 0.02
    N = int( 8000 * delay_sec )   # delay in samples
    # Buffer to store past signal values. Initialize to zero.
    BUFFER_LEN = N              # length of buffer
    buffer = BUFFER_LEN * [0]   # list of zeros
    # Open an output audio stream
    p = pyaudio.PyAudio()
    stream = p.open(format      = pyaudio.paInt16,
                    channels    = 1,
                    rate        = 8000,
                    input       = False,
                    output      = True )

    # Get first frame
    input_bytes = wf.readframes(1)
    # Initialize buffer index (circular index)
    k = 0
    while len(input_bytes) > 0:
        # Convert binary data to number
        x0, = struct.unpack('h', input_bytes)
        # Compute output value
        # y(n) = b0 x(n) + G x(n-N)
        y0 = b0 * x0 + G * buffer[k]
        # Update buffer
        buffer[k] = x0
        # Increment buffer index
        k = k + 1
        if k >= BUFFER_LEN:
            # The index has reached the end of the buffer. Circle the index back to the front.
            k = 0
        # Clip and convert output value to binary data
        y0= volume/100*y0
        output_bytes = struct.pack('h', int(clip16(y0)))
        # print(type(output_bytes))
        # Write output value to audio stream
        stream.write(output_bytes)
        # Get next frame
        input_bytes = wf.readframes(1)

    stream.stop_stream()
    stream.close()
    p.terminate()
    wf.close()

