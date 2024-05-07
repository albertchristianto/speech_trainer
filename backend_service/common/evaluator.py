import sys
sys.path.append(".")

import evaluate
from common.text_normalizer.en import en_normalizer
from common.text_normalizer.zh import zh_normalizer

class SpeechEvaluator:
  def __init__(self) -> None:
    self.metric = evaluate.load(f'common/cer.py')

  def preprocess_zh(self, sentences, out):
    for each_sntncs in sentences:
      new_str = ""
      for each_char in each_sntncs:
        new_str += each_char + " "
      new_str = zh_normalizer(new_str)
      out.append(new_str)
    return out

  def preprocess_en(self, sentences, out):
    for each_sntncs in sentences:
      each_sntncs = en_normalizer(each_sntncs)
      out.append(each_sntncs)
    return out

  def __call__(self, pred_strs, label_strs, lang) -> int:
    gt = []
    pred = []
    if lang == "zh":
      gt = self.preprocess_zh(label_strs, gt)
      pred = self.preprocess_zh(pred_strs, pred)
    elif lang == "en":
      gt = self.preprocess_en(label_strs, gt)
      pred = self.preprocess_en(pred_strs, pred)

    return 100 * self.metric.compute(predictions=pred, references=gt)

if __name__ == "__main__":
  speech_evaluator = SpeechEvaluator()
  pred_str = [ "豆乾排骨湯六粉",
               "揍幹排骨湯六粉",
               "豆乾排骨湯六份" ]
  label_str = [ "豆乾排骨湯六份",
                "豆乾排骨湯六份",
                "豆乾排骨湯六份"]
  print(speech_evaluator(pred_str, label_str, "zh"))
  pred_str = [ "tish is a test",
               "my name is you",
               "hello, friends" ]
  label_str = [ "this is a test",
                "my name is yoona",
                "hello friends" ]
  print(speech_evaluator(pred_str, label_str, "en"))