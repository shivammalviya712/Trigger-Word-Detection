"""All the crazy ideas are tested here."""

from pydub import AudioSegment
from pydub.playback import play


train = AudioSegment.from_wav('./dataset/activate/train/train2.wav')
play(train)