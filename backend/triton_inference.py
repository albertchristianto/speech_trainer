import numpy as np
import sounddevice as sd
import soundfile as sf
import torch
from common.triton_connection import get_triton_http_client_sync, httpclient
from kokoro import KModel, KPipeline
from kokoro.model import KModelForONNX


def load_input_ids(pipeline, text):
    if pipeline.lang_code in "ab":
        _, tokens = pipeline.g2p(text)
        for gs, ps, tks in pipeline.en_tokenize(tokens):
            if not ps:
                continue
    else:
        ps, _ = pipeline.g2p(text)

    if len(ps) > 510:
        ps = ps[:510]

    input_ids = list(
        filter(lambda i: i is not None, map(lambda p: pipeline.model.vocab.get(p), ps))
    )
    print(f"text: {text} -> phonemes: {ps} -> input_ids: {input_ids}")
    input_ids = torch.LongTensor([[0, *input_ids, 0]]).to(pipeline.model.device)
    return ps, input_ids


def load_voice(pipeline, voice, phonemes):
    pack = pipeline.load_voice(voice).to("cpu")
    return pack[len(phonemes) - 1]


def load_sample(model):
    pipeline = KPipeline(lang_code="a", model=model.kmodel, device="cpu")
    text = """
    In today's fast-paced tech world, building software applications has never been easier — thanks to AI-powered coding assistants.'
    """
    text = """
    The sky above the port was the color of television, tuned to a dead channel.
    """
    voice = "C:\\MyData\\speech_trainer\\debug\\voices\\af_heart.pt"

    pipeline = KPipeline(lang_code="z", model=model.kmodel, device="cpu")
    text = "甯，我很想妳。 我真的愛妳。給我機會來愛妳。我希望你立刻跟你男朋友分手，然後只屬於我。"
    voice = "C:\\MyData\\speech_trainer\\debug\\voices\\zf_xiaoyi.pt"

    phonemes, input_ids = load_input_ids(pipeline, text)
    style = load_voice(pipeline, voice, phonemes)
    speed = torch.IntTensor([1])

    return input_ids, style, speed


def inference_onnx():
    config_file = "C:\\Users\\Albert\\.cache\\huggingface\\hub\\models--hexgrad--Kokoro-82M\\snapshots\\f3ff3571791e39611d31c381e3a41a3af07b4987\\config-zh.json"
    checkpoint_path = "C:\\Users\\Albert\\.cache\\huggingface\\hub\\models--hexgrad--Kokoro-82M\\snapshots\\f3ff3571791e39611d31c381e3a41a3af07b4987\\kokoro-v1_1-zh.pth"

    kmodel = KModel(config=config_file, model=checkpoint_path, disable_complex=True)
    model = KModelForONNX(kmodel).eval()
    triton_session = get_triton_http_client_sync(url="192.168.0.16:4060")
    input_ids, style, speed = load_sample(model)

    # pad style
    style = torch.nn.functional.pad(style, (0, 256 - style.size(-1)), "constant", 0)
    inputs = [
        httpclient.InferInput("input_ids", [1, len(input_ids[0])], "INT64"),
        httpclient.InferInput("style", [1, 256], "FP32"),
        httpclient.InferInput("speed", [1], "INT32"),
    ]
    inputs[0].set_data_from_numpy(input_ids.numpy().astype(np.int64))
    inputs[1].set_data_from_numpy(style.numpy().astype(np.float32))
    inputs[2].set_data_from_numpy(speed.numpy().astype(np.int32))
    response = triton_session.infer(
        model_name="kokoro-model", inputs=inputs, outputs=[]
    )
    waveform = response.as_numpy("waveform")
    duration = response.as_numpy("duration")

    output = torch.from_numpy(waveform)
    print(f"output: {output.shape}")
    print(output)

    audio = output.numpy()
    sd.play(audio, 24000)
    sd.wait()
    sf.write("output.wav", audio, 24000)


if __name__ == "__main__":
    inference_onnx()
