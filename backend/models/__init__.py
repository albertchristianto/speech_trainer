import json

from models.stt import get_stt_models
from models.tts import get_tts_models


def load_speech_model(config_path):
    f = open(config_path)
    system_param = json.load(f)
    stt = get_stt_models(
        system_param["stt_model"],
        system_param["stt_weights_path"],
        (system_param["stt_use_gpu"] > 0),
    )
    tts = get_tts_models(
        system_param["tts_model"],
        system_param["tts_weights_path"],
        (system_param["tts_use_gpu"] > 0),
    )
    return stt, tts
