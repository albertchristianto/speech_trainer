import os
import sys
import time
import random
import uvicorn
from fastapi import File, UploadFile, FastAPI, HTTPException
from fastapi.responses import FileResponse

from loguru import logger

from models import load_speech_model
from common.utils import save_audio_file
from common.wer import wer
from common.text_normalizer.en import en_normalizer
from common.text_normalizer.zh import zh_normalizer

stt, tts = load_speech_model("cfgs/system.conf")
app = FastAPI()
TEMP_CACHE_PATH = "temp_cache"

@app.get("/generate_sample_audio")
def text_to_speech_generate(text: str, lang: str = "zh"):
  if not os.path.exists(TEMP_CACHE_PATH):
    os.makedirs(TEMP_CACHE_PATH)
  ref_wav_path = "rsc/female.mp3" if random.random() > 0.5 else "rsc/male.mp3"
  out_filename = f"{time.time()}_ning.wav"
  output_path = os.path.join(TEMP_CACHE_PATH, out_filename)
  try:
    the_wave = tts.forward(input_text=text, lang=lang, ref_wav_file_path=ref_wav_path)
    tts.to_wav(the_wave, output_path=output_path)
  except Exception as e:
    msg = "oops! what had just happened?!"
    logger.error(f"{msg}")
    logger.error(f"{e}")
    raise HTTPException(status_code=500, detail= f"{msg}\nHere is the the error message from the server for you to tell the admin!!!\n{e}")
  return FileResponse(path=output_path, media_type="audio/wav", filename=out_filename)

@app.post("/recognize_speech")
def speech_to_text_recognize(file: UploadFile = File(...), lang: str="zh"):
  if not os.path.exists(TEMP_CACHE_PATH):
    os.makedirs(TEMP_CACHE_PATH)
  ret, val = save_audio_file(file=file)# return file_name when successfully save the audio files
  if not ret:
    return { "text":"", "msg": val }
  try:
    res = stt.forward(val, lang=lang)
  except Exception as e:
    msg = "oops! what had just happened?!"
    logger.error(f"{msg}")
    logger.error(f"{e}")
    return { "text":"", "msg": f"{msg}\nHere is the the error message from the server for you to tell the admin!!!\n{e}"}
  return { "msg": "Success!", "text": res }

@app.get("/get_score")
def sentences_comparator(ground_truth: str, answer: str, lang: str):
  if (lang == "zh"):
    ground_truth = zh_normalizer(ground_truth)
    answer = zh_normalizer(answer)
  else:
    ground_truth = en_normalizer(ground_truth)
    answer = en_normalizer(answer)
  score = wer(ground_truth.split(), answer.split())
  return { "msg": "Success!", "score": score}

@app.get("/")
async def home(): 
  return { "msg": "The Backend Service of The Speech Trainer" }

if __name__ == "__main__":
  LOG_LEVEL = 'TRACE'
  logger.remove()
  logger.add(sys.stdout, level=LOG_LEVEL)

  uvicorn.run("main:app", reload=False, port=8000, host="0.0.0.0")
