import sys
sys.path.append('.')
import torch
from TTS.api import TTS
from loguru import logger

from models.tts import Text2SpeechInterface

class Tacotronv2(Text2SpeechInterface):
  def __init__(self, cfg):
    logger.trace('start the TTS engine!!')
    self._version = "Tacotron-v2"
    self.weights_path = { "zh": "tts_models/zh-CN/baker/tacotron2-DDC-GST",
                          "en": "tts_models/en/ljspeech/tacotron2-DDC" }
    device = "cuda" if ((cfg["tts_use_gpu"] == 1) and torch.cuda.is_available()) else "cpu" # Get device
    self.tts_handler = {}
    for key in self.weights_path:
      self.tts_handler[key] = TTS(self.weights_path[key])
      self.tts_handler[key].to(device)

  def t2s(self, input_text, gender="Male", output_path="tmp_audio/speech_output.wav", lang="zh"):#return the path of the output audio file
    input_text, ref_wav = self.preprocess_data(input_text, lang, gender)
    self.tts_handler[lang].tts_with_vc_to_file(input_text, speaker_wav=ref_wav, file_path=output_path)
    return output_path

if __name__ == '__main__':
  the_tts = Tacotronv2({"tts_use_gpu": 1 })
  the_tts.t2s("這是對文字轉語音技術的測試", gender="Male")
  the_tts.t2s("This is a test for text to speech technologies", gender="Female", output_path="tmp_audio/speech_output_1.wav", lang='en')
