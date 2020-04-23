"""All the files are integrated here."""

# Local files
from dataset import Dataset
from settings import Settings 


# Initialise settings
wake_sound = 'activate'
settings = Settings(wake_sound=wake_sound)
data = Dataset(settings=settings)
data.load_dataset()

# Check
print(data.X.shape)
print(data.Y.shape)