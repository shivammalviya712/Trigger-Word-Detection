"""All the files are integrated here."""

# Local files
from dataset import Dataset
from settings import Settings 
from model import model, load_model, train_model

# Initialise settings
wake_sound = 'activate'
settings = Settings(wake_sound=wake_sound)
data = Dataset(settings=settings)
data.load_dataset()
model = load_model()
loss, acc = model.evaluate(data.X_dev, data.Y_dev)

# Check
print("Dev set accuracy = ", acc)