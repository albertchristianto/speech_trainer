import opencc
import numpy as np
from faster_whisper import WhisperModel
from transformers import WhisperProcessor, WhisperForConditionalGeneration
import torch
from pydub import AudioSegment

from loguru import logger

class STT():
    def __init__(self, model_path=None, use_faster_whisper=True):
        self.model_path = model_path
        if model_path is not None:
            self.model_size = model_path
        else:
            # model_size = "large-v2"
            # model_size = "weights/whisper-small_finetuned_24102023"
            # model_size = "weights/whisper-small_finetuned_26102023"
            # model_size = "weights/whisper-small-finetuned_13112023"
            # model_size = "weights/whisper-small-finetuned_38-592_21112023_1700545612"
            # model_size = "weights/whisper-small-finetuned_15-56420233463035_28112023_1701125011"
            # model_size = "weights/whisper-small-01122023-finetuned_129-52937557674562_05122023_1701720794"
            # model_size = "weights/whisper-small-08122023-finetuned_152-5682418550044_12122023_1702359912"
            # model_size = "weights/whisper-small-15122023-finetuned_151-11482720178373_19122023_1702962079"
            self.model_size = "weights/whisper-small-22122023-150"
        self.use_faster_whisper = use_faster_whisper
        # if self.use_faster_whisper:
        self.model = WhisperModel(self.model_size, device="cuda", compute_type="float16")# Run on GPU with FP16
        # self.model = WhisperModel(model_size, device="cuda", compute_type="int8_float16")# or run on GPU with INT8
        # self.model = WhisperModel(model_size, device="cpu", compute_type="int8")# or run on CPU with INT8
        # else:
        #     self.model = WhisperForConditionalGeneration.from_pretrained(model_size, device_map="auto", local_files_only=True)
        #     self.processor = WhisperProcessor.from_pretrained(model_size, language=None, task="transcribe")
        #     self.model.config.forced_decoder_ids = None
        #     self.model.config.suppress_tokens = [] #['<|nothing|>']

        self.converter = opencc.OpenCC('s2tw.json')

    def version(self):
        if self.model_path is not None:
            return self.model_size
        return self.model_size.split('/')[1]

    def _infer_faster_whisper(self, path, lang):
        segments, info = self.model.transcribe(path, beam_size=5,language=lang, 
            vad_filter=True, vad_parameters=dict(min_silence_duration_ms=500))
        output = "".join([segment.text for segment in segments])
        output = self.converter.convert(output)
        return output, info.language, info.language_probability
    
    # def _infer_manual(self, audio_path):
    #     audio_segment = AudioSegment.from_mp3(audio_path)
    #     # convert to expected format
    #     if audio_segment.frame_rate != 16000: # 16 kHz
    #         audio_segment = audio_segment.set_frame_rate(16000)
    #     if audio_segment.sample_width != 2:   # int16
    #         audio_segment = audio_segment.set_sample_width(2)
    #     if audio_segment.channels != 1:       # mono
    #         audio_segment = audio_segment.set_channels(1)
    #     arr = np.array(audio_segment.get_array_of_samples())
    #     arr = arr.astype(np.float32)/32768.0
    #     input_features = self.processor(arr, sampling_rate=16000, return_tensors="pt").input_features
    #     outputs = self.model.generate(
    #         input_features, output_scores=True, return_dict_in_generate=True, max_new_tokens=128
    #     )

    #     transition_scores = self.model.compute_transition_scores(
    #         outputs.sequences, outputs.scores, normalize_logits=True
    #     )

    #     pred_text = self.processor.batch_decode(outputs.sequences, skip_special_tokens=True)
    #     pred_language = self.processor.batch_decode(outputs.sequences[:, 1:2], skip_special_tokens=False)
    #     lang_prob = torch.exp(transition_scores[:, 0])

    #     return pred_text, pred_language, lang_prob

    def s2t(self, path="./output.wav", lang=None):
        # if self.use_faster_whisper:
        output, pred_language, lang_prob = self._infer_faster_whisper(path, lang)
        # else:
        #     output, pred_language, lang_prob = self._infer_manual(path)
        logger.trace(f"Detected language {pred_language} with probability {lang_prob}")
        logger.trace(f"{output}")

        return { "text" : output, "filename": path, "language": pred_language }, pred_language, lang_prob

    def detect_newest(self):
        logger.warning("Not yet implemented!")
        #To do list:detect the newest model which is trained
        return None

if __name__ == '__main__':

    the_stt = STT()
    res = the_stt.s2t()
    print(res)
