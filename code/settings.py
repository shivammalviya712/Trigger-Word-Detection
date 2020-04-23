"""The important parameters are defined here."""


class Settings:
    """The important parameters are
    the attributes of this class. 
    """

    def __init__(self, wake_sound, Ty=1375, m=26):
        """
        # Arguments
            wake_Sound: String
                It tells whether we are going 
                to use activate or snap dataset.
            Ty: Integer
                The length of the output.
            m: Number of training examples to be created.
        """
        self.wake_sound = wake_sound
        self.Ty = Ty
        self.m = m

