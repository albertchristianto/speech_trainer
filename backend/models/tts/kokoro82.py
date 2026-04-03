import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), "../.."))
import opencc
import soundfile as sf
import torch
from kokoro import KPipeline
from loguru import logger

from models.tts.tts import Text2SpeechInterface


class Kokoro82(Text2SpeechInterface):
    converter = opencc.OpenCC("t2s.json")

    def __init__(self, use_gpu=True):
        logger.trace("start the TTS engine!!")
        self._version = "Kokoro-v1.0"
        self.lang = {
            "zh": "z",
            "en": "a",
        }
        self.voice = {
            # "zh": "zf_xiaoyi",
            "zh": "zm_yunjian",
            # "en": "af_heart",
            "en": "am_fenrir",
        }
        device = (
            "cuda" if (use_gpu and torch.cuda.is_available()) else "cpu"
        )  # Get device
        self.tts_handler = {}
        for key in self.lang:
            self.tts_handler[key] = KPipeline(lang_code=self.lang[key], device=device)

    def forward(
        self,
        input_text: str,
        lang: str,
        output_path: str = "temp_cache/speech_output.wav",
    ) -> str:
        input_text = self.preprocess_data(input_text, lang)
        generator = self.tts_handler[lang](input_text, voice=self.voice[lang])
        for _, _, audio in generator:
            sf.write(output_path, audio, 24000)
        return output_path

    def preprocess_data(self, input_text, lang):
        if lang == "zh":
            input_text = self.converter.convert(input_text)
        return input_text


if __name__ == "__main__":
    the_tts = Kokoro82(use_gpu=True)
    en_text = """
[Kokoro](/kˈOkəɹO/) is an open-weight TTS model with 82 million parameters. Despite its lightweight architecture, it delivers comparable quality to larger models while being significantly faster and more cost-efficient. With Apache-licensed weights, [Kokoro](/kˈOkəɹO/) can be deployed anywhere from production environments to personal projects.
"""
    the_tts.forward(en_text, lang="en", output_path="en_output.wav")
    zh_text = "甯，我很想妳。 我真的愛妳。給我機會來愛妳。我希望你立刻跟你男朋友分手，然後只屬於我。"
    the_tts.forward(zh_text, lang="zh", output_path="zh_output.wav")
