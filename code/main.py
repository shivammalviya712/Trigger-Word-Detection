"""All the files are integrated here."""

# Local files
from dataset import Dataset
from settings import Settings 
from model import model

# Initialise settings
wake_sound = 'activate'
settings = Settings(wake_sound=wake_sound)
data = Dataset(settings=settings)
data.load_dataset()
model = model(settings)
model.summary()