"""All the crazy ideas are 
brought to life, in this file
"""

import sounddevice as sd


duration = 10
fs = 44100
print('Start')
myrecording = sd.rec(frames = int(duration*fs), samplerate=fs, channels=2)
sd.wait()
sd.play(myrecording, fs)
sd.wait()
print('Good to go man')