import opencc

class Text2SpeechInterface:
  converter = opencc.OpenCC('t2s.json')
  punc_stop = [ ".", "！", "？", "｡", "。", '!', '?' ]

  def forward(self, input_text: str, lang: str, ref_wav_file_path: str) -> str:
    """Generate the wave and write the audio files into the path"""
    pass

  def preprocess_data(self, input_text, lang, gender):
    if lang in self.lang_code_converter.keys():
      lang = self.lang_code_converter[lang]
    ref_wav = f"rsc/{lang}_{gender}.wav"
    if lang == 'zh':
      input_text = self.converter.convert(input_text)
    input_text = self.adding_punctuation(input_text, lang)

    return input_text, ref_wav

  def adding_punctuation(self, input_text, lang):
    if input_text[-1] in self.punc_stop:
      return input_text
    if lang == "zh":
      return input_text + "。"
    elif lang == 'en':
      return input_text + "."

  def version(self):
    return self._version
