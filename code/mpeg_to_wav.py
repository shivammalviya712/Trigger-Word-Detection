import os
from pydub import AudioSegment

input_path = "./dataset/snap/snaps_mpeg"
output_path = "./dataset/snap/positives"
for i, filename in enumerate(os.listdir(input_file_path)):
    if filename.endswith("mpeg"):
        sound_mpeg = AudioSegment.from_mp3(file = input_file_path + "/" + filename)
        sound_mpeg.export(output_file_path + "/" + "train" + str(i) +".wav", format = "wav")

