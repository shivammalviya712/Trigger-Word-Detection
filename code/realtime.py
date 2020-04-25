"""Implement the model in real time."""

# Third party modules
import numpy as np
import sounddevice as sd
from pydub import AudioSegment


class Realtime:
    """TODO"""
    def __init__(self, data, model, settings):
        """TODO"""
        self.data = data
        self.model = model
        self.chime = AudioSegment.from_wav('./dataset/activate/chime/chime.wav')
        self.Ty = settings.Ty
        self.Tnew = settings.Tnew
        self.fs = settings.fs

        sd.default.samplerate = self.fs
        sd.default.channels = 2

    
    def record(self):
        """It records the audio
        from the inbuilt microphone.
        
        # Returns
            audio: ndarray
                The audio recorded.
        """
        audio = sd.rec(frames=int(self.Tnew*self.fs))
        # To be continued........................
        # ..........................................
        #........................................
        #...................................

    
    def detect_triggerword(self, filename):
        """Detects the trigger word
        in the given audio.
        
        # Arguments:
        # TODO
        """
        x = self.data.graph_spectrogram(filename)
        x = x.swapaxes(0, 1)
        x = np.expand_dims(x, axis=0)
        predictions = self.model.predict(x)

        return predictions


    def chime_on_activate(self, filename, predictions, threshold):
        """TODO"""
        audio_clip = AudioSegment.from_wav(filename)
        consecutive_timesteps = 0
        for i in range(self.Ty):
            consecutive_timesteps += 1
            if predictions[0, i, 0] > threshold and consecutive_timesteps > 75
            audio_clip = audio_clip.overlay(self.chime, position=((i/self.Ty) * audio_clip.duration_seconds)*1000)

        audio_clip.export(..................)
