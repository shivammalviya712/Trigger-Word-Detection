"""All the files are integrated here."""

# Local files
import keyboard
from settings import Settings 
from model import model, load_model, train_model
from realtime import Realtime


print('Everything is successfully imported')
settings = Settings()
print('Settings is done')
model = load_model()
print('Model is loaded')
realtime = Realtime(settings)
print('Realtime is done')

print('start')
while True:
    if keyboard.is_pressed('q'):
        break

    realtime.refresh_audio()
    y = model.predict(realtime.x)
    realtime.check_trigger(y)
    print('Done')
    