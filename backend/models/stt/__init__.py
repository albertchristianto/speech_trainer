from models.stt.whisper import Whisper


def get_stt_models(model_name, weight_dir_path, use_gpu):
    if model_name == "whisper":
        return Whisper(weight_dir_path, use_gpu)
    return None
