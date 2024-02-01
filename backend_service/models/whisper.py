import sys
sys.path.append('.')
import opencc
import numpy as np
from transformers import WhisperProcessor, WhisperForConditionalGeneration
from pydub import AudioSegment
from models.stt import Speech2TextInterface

class Whisper(Speech2TextInterface):
  def __init__(self, model_path="weights/whisper-small"):
    self.model = WhisperForConditionalGeneration.from_pretrained(model_path, device_map="auto")
    self.processor = WhisperProcessor.from_pretrained(model_path, language=None, task="transcribe")
    self.model.config.forced_decoder_ids = None
    self.model.config.suppress_tokens = [] #['<|nothing|>']
    self.converter = opencc.OpenCC('s2tw.json')

  def forward(self, path_to_audio_file: str, lang: str) -> str:
    audio_segment = AudioSegment.from_mp3(path_to_audio_file)
    # convert to expected format
    if audio_segment.frame_rate != 16000: # 16 kHz
      audio_segment = audio_segment.set_frame_rate(16000)
    if audio_segment.sample_width != 2:   # int16
      audio_segment = audio_segment.set_sample_width(2)
    if audio_segment.channels != 1:       # mono
      audio_segment = audio_segment.set_channels(1)
    arr = np.array(audio_segment.get_array_of_samples())
    arr = arr.astype(np.float32) / 32768.0
    input_features = self.processor(arr, sampling_rate=16000, return_tensors="pt").input_features.cuda()
    forced_decoder_ids = self.processor.get_decoder_prompt_ids(language=lang, task="transcribe")
    self.model.config.forced_decoder_ids = forced_decoder_ids
    outputs = self.model.generate(input_features)
    pred_text = self.processor.batch_decode(outputs, skip_special_tokens=True)

    return pred_text

if __name__ == '__main__':
  the_stt = Whisper()
  res = the_stt.forward("ref_voices/train/23092023/grace_guo.wav", "zh")
  with open('test.txt', 'w', encoding='utf8') as f:
    f.write(res[0])
