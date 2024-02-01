import numpy as np
from scipy.io import wavfile

class Text2SpeechInterface:
  def forward(self, input_text: str, lang: str, ref_wav_file_path: str) -> np.ndarray:
    """Generate the wave in numpy array"""
    pass

  def to_wav(self, input_, sampling_rate=24000, output_path='test.wav'):
    scaled = np.int16(input_ / np.max(np.abs(input_)) * 32767)#normalize the data first
    wavfile.write(output_path, sampling_rate, scaled)