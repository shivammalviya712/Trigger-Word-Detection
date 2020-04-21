"""The important parameters are defined here."""


class Settings:
    """The important parameters are
    the attributes of this class. 
    """

    def __init__(self, wake_sound, Ty=1365, seed=18):
        """
        # Arguments
            wake_Sound: String
                It tells whether we are going 
                to use activate or snap dataset.
            Ty: Integer
                The length of the output.
            seed: Integer
                The seed for generating the random numbers.
        """
        self.wake_sound = wake_sound
        self.Ty = Ty
        self.seed = seed

