import os
from pydub import AudioSegment

input_file_path = "./dataset/snaps_mpeg"
output_file_path = "./dataset/snaps_wav"
for i, filename in enumerate(os.listdir(input_file_path)):
    if filename.endswith("mpeg"):
        sound_mpeg = AudioSegment.from_mp3(file = input_file_path + "/" + filename)
        sound_mpeg.export(output_file_path + "/" + "train" + str(i) +".wav", format = "wav")

