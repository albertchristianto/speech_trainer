from loguru import logger
from TTS.api import TTS
import torch
import opencc

USE_TACOTRON_MODEL = True
CN_PUNCS_STOP = [ ".", "！", "？", "｡", "。" ]

class Text2Speech():
    def __init__(self):
        logger.trace('start the TTS engine!!')
        if USE_TACOTRON_MODEL:
            model_name = "tts_models/zh-CN/baker/tacotron2-DDC-GST"
        else:
            model_name = "tts_models/multilingual/multi-dataset/xtts_v2"
        device = "cuda" if torch.cuda.is_available() else "cpu" # Get device
        self.tts_handler = TTS(model_name)
        self.tts_handler.to(device)
        self.converter = opencc.OpenCC('t2s.json')

    def t2s(self, input_text, gender="Male", output_path="tmp_audio/speech_output.wav"):#return the path of the output audio file
        if gender == "Male":
            ref_wav = "rsc/male_ai.wav"
        else:
            ref_wav = "rsc/female_ai.wav"
        logger.trace(gender)
        input_text = self.adding_punctuation(input_text)
        input_text = self.converter.convert(input_text)
        if USE_TACOTRON_MODEL:
            self.tts_handler.tts_with_vc_to_file(input_text, speaker_wav=ref_wav, file_path=output_path)
        else:
            self.tts_handler.tts_to_file(text = input_text, file_path = output_path, speaker_wav = ref_wav, language = "zh-cn")
        return output_path

    def adding_punctuation(self, input_text):
        if input_text[-1] in CN_PUNCS_STOP:
            return input_text
        return input_text + "。"

if __name__ == '__main__':
    import time
    the_tts = Text2Speech()
    the_tts.t2s("好的!", gender="Female")
