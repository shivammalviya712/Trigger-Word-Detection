"""Load, synthesize, and preprocess the raw data"""

# Standard libraries
import os
import warnings

# Third party imports
import matplotlib.pyplot as plt
import numpy as np
from pydub import AudioSegment
from pydub.playback import play
from scipy.io import wavfile


# Disabling warnings
warnings.filterwarnings(action='ignore', category=RuntimeWarning)


class Dataset:
    def __init__(self, settings):
        """
        # Arguments 
            settings: Object of class Settings
                Important parameters are the attributes of this object.
        """    
        self.wake_sound = settings.wake_sound
        self.positives = []
        self.negatives = []
        self.backgrounds = []
        self.load_dataset()


    def graph_spectrogram(self, wav_file):
        """Plot the spectrogram for the given wav file.

        # Arguments
            wav_file: String
                Relative path to the audio file.

        # Returns:
            pxx: 2D array
                The periodograms of the successive segments. 
        """
        fs, x = wavfile.read(wav_file)
        nfft = 200
        nchannels = x.ndim
        if nchannels == 1:
            pxx, freqs, bins, im = plt.specgram(x=x, NFFT=nfft, Fs=fs)
        elif nchannels == 2:
            pxx, freqs, bins, im = plt.specgram(x=x[:, 0], NFFT=nfft, Fs=fs)
        else:
            print('The audio has more than 2 channels')       
        plt.show()

        return  pxx


    def load_dataset(self):  
        """Load the dataset.

        # Variables
            positives: List
                The list of all the recordings of the trigger word.
            negatives: List
                The list of all the recordings of the non-triger words.
            backgrounds: List
                The list of all the recordings of the background noise.
        """
        # Loading the positive words.
        for filename in os.listdir('./dataset/' + self.wake_sound + '/positives'):
            if filename.endswith('wav'):
                positive = AudioSegment.from_wav('./dataset/' + self.wake_sound + '/positives/' + filename)
                self.positives.append(positive)
        # Loading the negative words.
        for filename in os.listdir('./dataset/' + self.wake_sound + '/negatives'):
            if filename.endswith('wav'):
                negative = AudioSegment.from_wav('./dataset/' + self.wake_sound + '/negatives/' + filename)
                self.negatives.append(negative)
        # Loading the background noise.
        for filename in os.listdir('./dataset/' + self.wake_sound + '/backgrounds'):
            if filename.endswith('wav'):
                background = AudioSegment.from_wav('./dataset/' + self.wake_sound + '/backgrounds/' + filename)
                self.backgrounds.append(background)


    def get_random_time_segment(self, segment_len, background_len):
        """Gets random time segment of length 
        segment_len in the audio clip of background_len.

        # Arguments
            segment_len: The length of the required random segment.
            background_len: The length of the background noise.

        # Returns
            segment_start: The start of the random segment.
            segment_end: The end of the random segment.
        """ 
        # Distribution is [low, high)
        # One is added because later, one will be subracted from segment_end. 
        segment_start = np.random.randint(low=0, high=background_len-segment_len+1)
        # One is subracted because the starting will also be included.
        segment_end = segment_start + segment_len - 1

        return segment_start, segment_end


    def is_overlapping(self, segment, previous_segments):
        """Check whether the segment overlap 
        with the previous segments or not.

        # Arguments
            segment: a tuple
                (segment_start, segment_end)
            previous_segment: a list of tuples
                list of existing segments

        # Return
            overlap: Flag variable
                Tells whether the segment overlaps 
                with the previous segments or not.
        """
        segment_start, segment_end = segment
        # Flag for overlap
        overlap = False
        for previous_start, previous_end in previous_segments:
            if segment_start <= previous_end and previous_start <= segment_end:
                overlap = True

        return overlap