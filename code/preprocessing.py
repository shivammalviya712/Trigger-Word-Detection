import os
from pydub import AudioSegment
from pydub.playback import play
from scipy.io import wavfile
import matplotlib.pyplot as plt
import warnings

warnings.filterwarnings(action="ignore", category=RuntimeWarning)

input_file_path = "./dataset/snaps_wav"
for filename in os.listdir(path = input_file_path):
    if filename == "train1.wav":
        fs, x = wavfile.read(filename = input_file_path + "/" + filename)
        nfft = 200
        nchannels = x.ndim

        if nchannels == 1:
            pxx, freqs, bins, im = plt.specgram(x = x, NFFT = nfft, Fs = fs)
        
        elif nchannels == 2:
            pxx, freqs, bins, im = plt.specgram(x = x[:, 0], NFFT = nfft, Fs = fs)

        else:
            print("The audio has more than 2 channels")       

        plt.show() 