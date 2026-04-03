from models.tts.kokoro82 import Kokoro82


def get_tts_models(model_name, weight_dir_path, use_gpu):
    if model_name == "kokoro":
        return Kokoro82(use_gpu)
    return None
