import os
from TTS.api import TTS

os.environ["COQUI_TOS_AGREED"] = "1"
device = "cpu"

def clone(text, audio, output_file):
    tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2").to(device)
    tts.tts_to_file(text=text, speaker_wav=audio, language="en", file_path=output_file)
