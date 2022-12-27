import pyaudio
import wave
import struct
import math

def clip16( x ):
    # Clipping for 16 bits
    if x > 32767:
        x = 32767
    elif x < -32768:
        x = -32768
    else:
        x = x
    return(x)

def play(single_note,volume,W):
    wavfile = 'Note'+str(single_note+1)+'.wav'
    # Open the wave file
    wf = wave.open( wavfile, 'rb')
    # Vibrato parameters
    f0 = 2
    # Buffer to store past signal values. Initialize to zero.
    BUFFER_LEN =  512          # Set buffer length.
    buffer = BUFFER_LEN * [0]   # list of zeros
    # Initialize buffer indices
    kr = int(0.5 * BUFFER_LEN)  # read index
    kw = 0                      # write index

    # Open an output audio stream
    p = pyaudio.PyAudio()
    stream = p.open(format      = pyaudio.paInt16,
                    channels    = 1,
                    rate        = 8000,
                    input       = False,
                    output      = True )

    # Loop through wave file
    for n in range(0, 4000):
        # Get sample from wave file
        input_bytes = wf.readframes(1)

        # Convert string to number
        x0, = struct.unpack('h', input_bytes)

        # Compute output value - time-varying delay, no direct path
        y0 = buffer[int(kr)]  # use int() for integer

        # Update buffer
        buffer[kw] = x0

        # Increment read index
        kr = kr + 1 + W * math.sin( 2 * math.pi * f0 * n / 8000 )
        # Note: kr is not integer!

        # Ensure that 0 <= kr < BUFFER_LEN
        if kr >= BUFFER_LEN:
            # End of buffer. Circle back to front.
            kr = kr - BUFFER_LEN

        # Increment write index
        kw = kw + 1
        if kw == BUFFER_LEN:
            # End of buffer. Circle back to front.
            kw = 0

        #volume as 0%-100%
        y0= volume/100*y0
        # Clip and convert output value to binary data
        output_bytes = struct.pack('h', int(clip16(y0)))
        # Write output to audio stream
        stream.write(output_bytes)

    stream.stop_stream()
    stream.close()
    p.terminate()
    wf.close()
