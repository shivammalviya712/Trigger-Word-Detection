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
        self.Ty = settings.Ty
        self.m = settings.m
        self.positives = []
        self.negatives = []
        self.backgrounds = []
        self.X = []
        self.Y = []
        self.X_dev = []
        self.Y_dev = []

    def graph_spectrogram(self, wav_file, plotting=False):
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
        noverlap = 120
        nchannels = x.ndim
        if nchannels == 1:
            pxx, freqs, bins, im = plt.specgram(
                x=x, NFFT=nfft, Fs=fs, noverlap=noverlap)
        elif nchannels == 2:
            pxx, freqs, bins, im = plt.specgram(
                x=x[:, 0], NFFT=nfft, Fs=fs, noverlap=noverlap)
        else:
            print('The audio has more than 2 channels')       
        
        if plotting==True:
            plt.show(block=False)
            plt.pause(0.001)

        return  pxx


    def match_target_amplitude(self, sound, target_dBFS):
        """It standardise volume of the audio clip.

        # Arguments
            sound: The audio clip to be standardise.
            target_dBFS: The standardize amplitude in dBFS.

        # Returns
            sound: The standardise audio clip.
        """
        change_in_dBFS = target_dBFS - sound.dBFS
        sound = sound.apply_gain(change_in_dBFS)
        
        return sound


    def load_raw_dataset(self):  
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
        for filename in os.listdir(
                './dataset/' + self.wake_sound + '/positives'):
            if filename.endswith('wav'):
                positive = AudioSegment.from_wav(
                    './dataset/' + self.wake_sound + '/positives/' + filename)
                self.positives.append(positive)
        # Loading the negative words.
        for filename in os.listdir(
                './dataset/' + self.wake_sound + '/negatives'):
            if filename.endswith('wav'):
                negative = AudioSegment.from_wav(
                    './dataset/' + self.wake_sound + '/negatives/' + filename)
                self.negatives.append(negative)
        # Loading the background noise.
        for filename in os.listdir(
                './dataset/' + self.wake_sound + '/backgrounds'):
            if filename.endswith('wav'):
                background = AudioSegment.from_wav(
                    './dataset/' + self.wake_sound + '/backgrounds/' + filename)
                self.backgrounds.append(background)


    def get_random_time_segment(self, segment_len):
        """Gets random time segment of length 
        segment_len in the background audio.

        # Arguments
            segment_len: The length of the required random segment.

        # Returns
            segment_start: The start of the random segment.
            segment_end: The end of the random segment.
        """ 
        # Distribution is [low, high)
        # One is added because later, one will be subracted from segment_end. 
        segment_start = np.random.randint(
            low=0, high=len(self.backgrounds[0])-segment_len+1)
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

    
    def insert_audio_clip(self, background, audio_clip, previous_segments):
        """Insert a new audio segment over the background 
        noise at a random time step, ensuring that the 
        audio segment does not overlap with existing segments.

        # Arguments
            background: Audio
                Background audio recording with the
                overlaped previous segments.
            audio_clip: Audio 
                Audio to be overlaped with the background.
            previous_segment: List of tuples
                The time where audios have already been inserted.

        # Returns:
            new_background: Audio
                The updated background audio.
            segment_time: Tuple
                (segment_start, segment_end) 
        """
        segment_len = len(audio_clip)
        segment_time = self.get_random_time_segment(segment_len)
        while self.is_overlapping(segment_time, previous_segments):
            segment_time = self.get_random_time_segment(segment_len)
        previous_segments.append(segment_time)
        new_background = background.overlay(audio_clip, position=segment_time[0])

        return new_background, segment_time
        
    
    def insert_ones(self, y, segment_end):
        """Update the label vector y. The labels of the 50 
        output steps strictly after the end of the segment 
        should be set to 1.

        # Arguments
            y: numpy array of shape (1, Ty)
                The label of training example.
            segment_end: Integer
                The end time of the segment in milliseconds.
        """
        segment_end_y = int(segment_end*self.Ty/10000)
        for j in range(segment_end_y+1, segment_end_y+51):
            if j < self.Ty:
                y[0, j] = 1

    
    def create_training_example(self, background, i):
        """Creates a training example with a 
        given background, positives, and negatives.
    
        # Arguments
            background: Audio
                A audio clip of background noise.
            i: Integer 
                Index of training example.

        # Returns
            x: 
                The spectrogram of the training example.
            y: 
                The label at each time step of the spectrogram.
        """ 
        # Make the background quitter.
        background = background - 20       
        y = np.zeros((1, self.Ty))
        previous_segments = []
        
        # Select 0-4 random "positives" audio clips.
        number_of_positives = np.random.randint(low=0, high=5)
        random_indices = np.random.randint(low=0, high=len(self.positives),
                                           size=number_of_positives)
        random_positives = [self.positives[j] for j in random_indices]
        # Inserting the random_positives in the background.
        for random_positive in random_positives:
            background, segment_time = self.insert_audio_clip(
                background, random_positive, previous_segments)
            segment_start, segment_end = segment_time
            self.insert_ones(y, segment_end)
        
        # Select 0-2 random negtives audio clips.
        number_of_negatives = np.random.randint(low=0, high=3)
        random_indices = np.random.randint(low=0, high=len(self.negatives), 
                                           size=number_of_negatives)
        random_negatives = [self.negatives[j] for j in random_indices]
        # Inserting the random_negatives in the background.
        for random_negative in random_negatives:
            background, _ = self.insert_audio_clip(
                background, random_negative, previous_segments)
        
        background = self.match_target_amplitude(background, -20.0)
        file_handle = background.export(
            './dataset/' + self.wake_sound + '/train/train' + str(i) + '.wav', format='wav')
        print('File (train' + str(i) + '.wav) was saved in your directory.')
        x = self.graph_spectrogram(
            wav_file='./dataset/' + self.wake_sound + '/train/train' + str(i) + '.wav', plotting=False)

        return x, y


    def create_training_examples(self):
        """It creates the whole training data
        and saves it in X.npy and Y.npy. 
        """
        self.load_raw_dataset()
        for i in range(self.m):
            random_index = np.random.randint(low=0, high=len(self.backgrounds))
            background = self.backgrounds[random_index]
            x, y = self.create_training_example(background, i)
            self.X.append(x.T)
            self.Y.append(y.T)
        self.X = np.array(self.X)
        self.Y = np.array(self.Y)
        np.save(file='./dataset/' + self.wake_sound + '/train/X.npy', arr=self.X)
        np.save(file='./dataset/' + self.wake_sound + '/train/Y.npy', arr=self.Y)


    def load_dataset(self):
        """Loads the dataset prepared and saved 
        in advance in the file X.npy and Y.npy
        """
        self.X = np.load(file='./dataset/' + self.wake_sound + '/train/X.npy')
        self.Y = np.load(file='./dataset/' + self.wake_sound + '/train/Y.npy')
        self.X_dev = np.load(file='./dataset/' + self.wake_sound + '/dev/X_dev.npy')
        self.Y_dev = np.load(file='./dataset/' + self.wake_sound + '/dev/Y_dev.npy')
