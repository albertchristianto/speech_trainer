import opencc
import random

class Text2SpeechInterface:
  converter = opencc.OpenCC('t2s.json')
  punc_stop = [ ".", "！", "？", "｡", "。", '!', '?' ]

  def forward(self, input_text: str, lang: str, output_path: str) -> str:
    """Generate the wave and write the audio files into the path"""
    pass

  def preprocess_data(self, input_text, lang):
    if lang == 'zh':
      input_text = self.converter.convert(input_text)
    ref_wav_path = f"rsc/{lang}_female.wav" if random.random() > 0.5 else f"rsc/{lang}_male.wav"
    input_text = self.adding_punctuation(input_text, lang)
    return input_text, ref_wav_path

  def adding_punctuation(self, input_text, lang):
    if input_text[-1] in self.punc_stop:
      return input_text
    if lang == "zh":
      return input_text + "。"
    elif lang == 'en':
      return input_text + "."

  def version(self):
    return self._version
