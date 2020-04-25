"""The important parameters are defined here."""


class Settings:
    """The important parameters are
    the attributes of this class. 
    """

    def __init__(self, wake_sound, Ty=1375, Tx=5511, 
                 fs=44100, n_freq=101, m=26, Tnew=0.25):
        """
        # Arguments
            wake_Sound: String
                It tells whether we are going 
                to use activate or snap dataset.
            Ty: Integer
                The length of the output.
            Tx: Integer
                The length of the input.
            fs: Integer
                Sampling frequency at which audio
                will be recorded from the microphone.
            n_freq: Integer
                Number of frequencies in spectrogram.
            m: Integer
                Number of training examples to be created.
            Tnew: Integer
                Time in seconds of new audio
                added to the 10sec frame.
        """
        self.wake_sound = wake_sound
        self.Ty = Ty
        self.Tx = Tx
        self.fs = fs
        self.n_freq = n_freq
        self.m = m
        self.Tnew = Tnew