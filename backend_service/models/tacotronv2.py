import sys
sys.path.append('.')
import torch
from TTS.api import TTS
from loguru import logger

from models.tts import Text2SpeechInterface

class Tacotronv2(Text2SpeechInterface):
  def __init__(self, weight_dir_path="weights/xttsv2/", use_gpu=True):
    logger.trace('start the TTS engine!!')
    self._version = "Tacotron-v2"
    self.weights_path = { "zh": "tts_models/zh-CN/baker/tacotron2-DDC-GST",
                          "en": "tts_models/en/ljspeech/tacotron2-DDC" }
    device = "cuda" if (use_gpu and torch.cuda.is_available()) else "cpu" # Get device
    self.tts_handler = {}
    for key in self.weights_path:
      self.tts_handler[key] = TTS(self.weights_path[key])
      self.tts_handler[key].to(device)

  def forward(self, input_text: str, lang: str, output_path: str="temp_cache/speech_output.wav") -> str:
    input_text, ref_wav_path = self.preprocess_data(input_text, lang)
    self.tts_handler[lang].tts_to_file(input_text, speaker_wav=ref_wav_path, file_path=output_path)
    return output_path

if __name__ == '__main__':
  the_tts = Tacotronv2({"tts_use_gpu": 1 })
  the_tts.forward("這是對文字轉語音技術的測試", lang='zh')
  the_tts.forward("This is a test for text to speech technologies", lang='en')