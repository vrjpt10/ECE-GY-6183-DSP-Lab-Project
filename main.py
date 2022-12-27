import sys
sys.path.append('other')
from Detection import Detection
from Webcam import Webcam
import pyaudio, struct
from struct import pack
from math import sin, cos, pi
import tkinter as Tk
import time
import math
import wave
import No_effect
import Echo_effect
import Vibrato_effect


#GUI part
def piano_start():
    global opencamera
    print('Start Camera!')
    opencamera = True

def piano_quit():
    global Continue
    print('Good bye!')
    Continue = False

# Define Tkinter root
root = Tk.Tk()
root.title("Virtual Piano Setting")
Tk.Label(root, text="Notes:",font=('Arial',16),fg='green').pack()

#Initialize Tk variable
f0 = Tk.DoubleVar()
f0.set(262)
#Set C note at 262Hz
f1 = Tk.DoubleVar()
f1.set(50)
#Set Volumn as 50%
f2 = Tk.DoubleVar()
f2.set(0.2)
#Set Vibrato parameter as 0.2

var = Tk.StringVar()
var.set("Traditional")
var1 = Tk.StringVar()
var1.set("No")
var2 = Tk.StringVar()
var2.set("Close")


#Define handlers for GUI:

def handler():
    print ("Notes mode selected: " + str(var.get()))
def handler1():
    print ("Sound mode selected: " + str(var1.get())+" Effect")
def handler2():
    global opencamera
    if var2.get()== 'Close':
        opencamera = False
    if var2.get()== 'Open':
        opencamera = True

R1 = Tk.Radiobutton(root, text = "Traditional Note", variable = var, value = 'Traditional',
                    command = handler)
R2 = Tk.Radiobutton(root, text = "DIY Note", variable = var, value = 'DIY',
                    command = handler)
S1 = Tk.Scale(root,  variable = f0, from_ = 150, to = 450,  resolution = 1,orient='horizontal')
S2 = Tk.Scale(root, label = 'Volume(%):', variable = f1, from_ = 0.0, to = 100.0, resolution = 1,orient='horizontal')
R3 = Tk.Radiobutton(root, text = "No Effect", variable = var1, value = 'No',
                    command = handler1)
R4 = Tk.Radiobutton(root, text = "Echo Effect", variable = var1, value = 'Echo',
                    command = handler1)
R5 = Tk.Radiobutton(root, text = "Vibrato Effect", variable = var1, value = 'Vibrato',
                    command = handler1)
S3 = Tk.Scale(root, variable = f2, from_ = 0.0, to = 1.0, resolution = 0.01,orient='horizontal')
# button = Tk.Button(root, text='Start Camera', width=25, command=piano_start())
# B_quit = Tk.Button(root, text = 'Quit', width=25,command = piano_quit())
R6 = Tk.Radiobutton(root, text = "Set All Parameters Above First", variable = var2, value = 'Close',
                    command = handler2)
R7 = Tk.Radiobutton(root, text = "Start Camera Then", variable = var2, value = 'Open',
                    command = handler2)

# Place widgets
R1.pack()
R2.pack()
Tk.Label(root, text="Set f0 (For DIY note):").pack()
S1.pack()

Tk.Label(root, text="Volume:",font=('Arial',16),fg='green').pack()
S2.pack()
Tk.Label(root, text="Effects:",font=('Arial',16),fg='green').pack()
R3.pack()
R4.pack()

# button.pack(
# )
# B_quit.pack()
R5.pack()
Tk.Label(root, text='Vibrato Parameter W:').pack()
S3.pack()
Tk.Label(root, text="________________________________",font=('Arial',16),fg='green').pack()
R6.pack()
R7.pack()

#Play part
Continue = True
opencamera = False

#DIY notes by f0
def DIY(freq_base):
    f1 = freq_base
    f2 = freq_base * math.pow(2,(2.0/12.0))
    f3 = freq_base * math.pow(2,(4.0/12.0))
    f4 = freq_base * math.pow(2,(5.0/12.0))
    f5 = freq_base * math.pow(2,(7.0/12.0))
    f6 = freq_base * math.pow(2,(9.0/12.0))
    f7 = freq_base * math.pow(2,(11.0/12.0))
    Note=[f1,f2,f3,f4,f5,f6,f7]
    return Note

#Generate notes files for echo/vibrato effect
def Generate_notefiles(Note):
    Fs = 8000
    # Write a mono wave file
    for i in range(0,7):
        wf = wave.open('Note'+str(i+1)+'.wav', 'w')		# wf : wave file
        wf.setnchannels(1)			# one channel (mono)
        wf.setsampwidth(2)			# two bytes per sample (16 bits per sample)
        wf.setframerate(Fs)			# samples per second
        A = 2**15 - 1.0 			# amplitude
        f = Note[i]					# frequency in Hz
        N = int(0.5*Fs)
        for n in range(0, N):
            x = A * cos(2*pi*f/Fs*n)       	# signal value (float)
            byte_string = pack('h', int(x))
            # 'h' stands for 'short integer' (16 bits)
            wf.writeframes(byte_string)
        wf.close()

print('Set all the parameters then start the camera')

while Continue:
    root.update()
    freq_base = f0.get()
    volume = f1.get()
    note_length = 3

    #set notes first
    if var.get()=="Traditional":
        Note = DIY(262)
    if var.get()=="DIY":
        freq_base = f0.get()
        Note = DIY(freq_base)

    #if no effect
    if var1.get() == "No":
        while opencamera:
            print('Start camera')
            webcam = Webcam()
            webcam.start()
            image = webcam.get_current_frame()
            detection = Detection(image)
            playsound = True
            p = pyaudio.PyAudio()
            while True:
                image = webcam.get_current_frame()
                single_note = detection.get_active_cell(image)
                #Get most-active cell for play
                if single_note == None:
                    continue

                # playsound
                if playsound:
                    No_effect.play(Note,single_note,note_length,volume)
                    print("playing",single_note+1)
                    time.sleep(1)
                playsound = not playsound

    # if echo effect
    if var1.get() == "Echo":
        Generate_notefiles(Note)
        while opencamera:
            print('Start camera')
            webcam = Webcam()
            webcam.start()
            image = webcam.get_current_frame()
            detection = Detection(image)
            playsound = True
            p = pyaudio.PyAudio()
            while True:
                image = webcam.get_current_frame()
                single_note = detection.get_active_cell(image)
                #Get most-active cell for play
                if single_note == None:
                    continue

                # playsound
                if playsound:
                    Echo_effect.play(single_note,volume)
                    print("playing",single_note+1)
                    time.sleep(1)
                playsound = not playsound

    # if vibrato effect
    if var1.get() == "Vibrato":
        Generate_notefiles(Note)
        W = f2.get()
        # when W = 0 no effect'
        while opencamera:
            print('Start camera')
            webcam = Webcam()
            webcam.start()
            image = webcam.get_current_frame()
            detection = Detection(image)
            playsound = True
            p = pyaudio.PyAudio()
            while True:
                image = webcam.get_current_frame()
                single_note = detection.get_active_cell(image)
                #Get most-active cell for play
                if single_note == None:
                    continue
                    
                # playsound
                if playsound:
                    Vibrato_effect.play(single_note,volume,W)
                    print("playing",single_note+1)
                    time.sleep(1)
                playsound = not playsound
