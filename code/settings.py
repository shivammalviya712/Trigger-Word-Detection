"""The important parameters are defined here."""


class Settings:
    """The important parameters are
    the attributes of this class. 
    """

    def __init__(self):
        """
        # Attributes
            wake_sound: String
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
            duration: Integer
                Time in seconds to be feed into
                the model.
            threshold: Integer
                The value of y above which model
                will predict it to be a trigger.
        """
        self.wake_sound = 'activate'
        self.Ty = 1375
        self.Tx = 5511
        self.fs = 44100
        self.n_freq = 101
        self.m = 26
        self.Tnew = 10
        self.duration = 10
        self.threshold = 0.4