"""All the crazy ideas are 
brought to life, in this file
"""

from settings import Settings
from realtime import Realtime
import sounddevice as sd
import matplotlib.pyplot as plt


settings = Settings()
realtime = Realtime(settings)

fs = 44100
duration = 10

sd.default.samplerate = 44100
sd.default.channels = 2
sd.default.device = '0'

sound = sd.rec(frames = int(duration * fs))
sd.wait()
sd.play(sound)
sd.wait()



