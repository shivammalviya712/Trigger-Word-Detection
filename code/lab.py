"""All the crazy ideas are 
brought to life, in this file
"""

# Local files
import keyboard
from dataset import Dataset
from settings import Settings
from model import model, load_model, train_model


print('Everything is successfully imported')
settings = Settings()
print('Settings is done')
data = Dataset(settings)
data.load_dataset()
print('Data loaded')
model = model(settings)
train_model(model, data)
print('Model is trained')