
from TTS.tts.configs.xtts_config import XttsConfig
from TTS.tts.models.xtts import Xtts

config = XttsConfig()
config.load_json("weights/xttsv2/config.json")
model = Xtts.init_from_config(config)
model.load_checkpoint(config, checkpoint_dir="weights/xttsv2/", eval=True)
model.cuda()

outputs = model.synthesize(
    "It took me quite a long time to develop a voice and now that I have it I am not going to be silent.",
    config,
    speaker_wav="models/annie_898_2.wav",
    gpt_cond_len=3,
    language="en",
)
print(outputs)