from pydub import AudioSegment
from pydub.playback import play

train = AudioSegment.from_wav(file = "./dataset/train.wav")
play(train)