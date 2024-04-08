import sys
sys.path.append('.')
import os
import torch
import torchaudio
import numpy as np
from TTS.tts.configs.xtts_config import XttsConfig
from TTS.tts.models.xtts import Xtts

from models.tts import Text2SpeechInterface

class XttsV2(Text2SpeechInterface):
  def __init__(self, weight_dir_path="weights/xttsv2/", use_gpu=True):
    self.config = XttsConfig()
    self.config.load_json(os.path.join(weight_dir_path, "config.json"))
    self.model = Xtts.init_from_config(self.config)
    self.model.load_checkpoint(self.config, checkpoint_dir=weight_dir_path, eval=True)
    if torch.cuda.is_available() and use_gpu:
      self.model.cuda()

  def forward(self, input_text: str, lang: str, output_path: str="temp_cache/speech_output.wav") -> str:
    input_text, ref_wav_path = self.preprocess_data(input_text, lang)
    outputs = self.model.synthesize(input_text, self.config, speaker_wav=ref_wav_path, gpt_cond_len=0.2,
                                    language=lang, num_beams=2, length_penalty=0.8, speed=0.9)
    torchaudio.save(output_path, torch.tensor(outputs["wav"]).unsqueeze(0), 24000)
    return output_path

if __name__ == '__main__':
  the_model = XttsV2()
  # the_audio_file = the_model.forward("我愛你,許甯","zh")
  the_audio_file = the_model.forward("這是對文字轉語音技術的測試", lang='zh')
  the_audio_file = the_model.forward("This is a test for text to speech technologies", lang='en')