"""Implement the model in real time."""

# Third party modules
import matplotlib.pyplot as plt
import numpy as np
import sounddevice as sd
from pydub import AudioSegment


class Realtime:
    """TODO"""
    def __init__(self, settings):
        """Intiallise the attributes."""
        self.Ty = settings.Ty
        self.Tx = settings.Tx
        self.Tnew = settings.Tnew
        self.n_freq = settings.n_freq
        self.fs = settings.fs
        self.duration = settings.duration
        self.threshold = settings.threshold
        self.chime = AudioSegment.from_wav(
            './dataset/activate/chime/chime.wav')
        self.x = np.zeros((1, self.Tx, self.n_freq))
        self.new_audio = np.zeros(shape=(int(self.Tnew * self.fs), 2))

        sd.default.samplerate = self.fs
        sd.default.channels = 2

    
    def refresh_audio(self):
        """It adds spectrogram of new audio 
        to the x.
        """
        sd.wait()
        new_x = self.spectrogram(self.new_audio).T
        self.new_audio = sd.rec(frames=int(self.Tnew * self.fs))
        self.x[0, :self.Tx-len(new_x)] = self.x[0, len(new_x):]
        self.x[0, self.Tx-len(new_x):] = new_x



    def spectrogram(self, sound, plotting=False):
        """It generates the spectrogram 
        of the sound given.
        
        # Arguments
            sound: ndarray
                The recorded sound.

        # Returns
            x: ndarray
                The spectrogram of the sound.
        """
        nfft = 200
        noverlap = 120
        nchannels = sound.ndim
        if nchannels == 1:
            x, freqs, bins, im = plt.specgram(
                x=sound, NFFT=nfft, Fs=self.fs, noverlap=noverlap)
        elif nchannels == 2:
            x, freqs, bins, im = plt.specgram(
                x=sound[:, 0], NFFT=nfft, Fs=self.fs, noverlap=noverlap)
        else:
            print('The audio has more than 2 channels')       
        
        if plotting==True:
            plt.show(block=False)
            plt.pause(0.001)

        return  x


    def check_trigger(self, y):
        """It checks if wake word is
        predicted or not. If the wake
        word is present then it produces
        a chime sound.
        
        # Arguments
            y: ndarray
                Prediction of our model for
                Realtime.x as the input.
        """
        plt.plot(y[0,:,0])
        plt.ylabel('probability')
            