import sys
sys.path.append('.')
import os
import torch
import opencc
import numpy as np
from TTS.tts.configs.xtts_config import XttsConfig
from TTS.tts.models.xtts import Xtts

from models.tts import Text2SpeechInterface

class XttsV2(Text2SpeechInterface):
  def __init__(self, weight_dir_path="weights/xttsv2/", use_gpu=True):
    self.zh_punc_stop = [ ".", "！", "？", "｡", "。" ]
    self.converter = opencc.OpenCC('t2s.json')
    self.config = XttsConfig()
    self.config.load_json(os.path.join(weight_dir_path, "config.json"))
    self.model = Xtts.init_from_config(self.config)
    self.model.load_checkpoint(self.config, checkpoint_dir=weight_dir_path, eval=True)
    if torch.cuda.is_available() and use_gpu:
      self.model.cuda()

  def adding_punctuation(self, input_text):
    if input_text[-1] in self.zh_punc_stop:
      return input_text
    return input_text + "。"

  def forward(self, input_text: str, lang: str, ref_wav_file_path: str="ref_voices/test/28112023/annie_898_2.wav") -> np.ndarray:
    input_text = self.adding_punctuation(input_text)
    outputs = self.model.synthesize(input_text, self.config, speaker_wav=ref_wav_file_path, gpt_cond_len=0.2,
                                    language=lang, num_beams=2, length_penalty=0.8, speed=0.9)
    return outputs['wav']

if __name__ == '__main__':
  the_model = XttsV2()
  the_wave = the_model.forward("我愛你,許甯","zh")
  the_model.to_wav(the_wave)