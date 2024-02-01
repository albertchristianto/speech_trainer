import sys
sys.path.append('.')
import json
from models.whisper import Whisper
from models.xttsv2 import XttsV2
import time

def get_tts_models(model_name, weight_dir_path, use_gpu):
  if model_name == "xttsv2":
    return XttsV2(weight_dir_path, use_gpu)
  return None

def get_stt_models(model_name, weight_dir_path):
  if model_name == "whisper":
    return Whisper(weight_dir_path)
  return None

def load_speech_model(config_path):
  f = open(config_path)
  system_param = json.load(f)
  stt = get_stt_models(system_param['stt_model'], system_param['stt_weights_path'])
  tts = get_tts_models(system_param['tts_model'], system_param['tts_weights_path'], (system_param['tts_use_gpu'] > 0))
  return stt, tts

if __name__ == '__main__':
  config_path = "cfgs/system.conf"
  stt, tts = load_speech_model(config_path)
  time.sleep(10)