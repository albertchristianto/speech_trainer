import os
import sys
import time
import uvicorn

from contextlib import asynccontextmanager
from fastapi import File, UploadFile, FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware

from loguru import logger

from models import load_speech_model
from common.utils import save_audio_file
from common.evaluator import SpeechEvaluator
from common.text_normalizer.en import en_normalizer
from common.text_normalizer.zh import zh_normalizer

dl_models = {}
TEMP_CACHE_PATH = "temp_cache"

@asynccontextmanager
async def lifespan(app: FastAPI):
  # Load the ML model
  dl_models["stt"], dl_models["tts"] = load_speech_model("cfgs/system.conf")
  dl_models["cer"] = SpeechEvaluator()
  yield
  # Clean up the ML models and release the resources
  dl_models.clear()

app = FastAPI(lifespan=lifespan)
origins = ["http://localhost:3000"]# Allow only requests from localhost:3000
app.add_middleware(CORSMiddleware, allow_origins=origins, allow_credentials=True, allow_methods=["*"], allow_headers=["*"])# Include CORS middleware

@app.get("/generate_sample_audio", summary="Text to Speech Engine", description="Generate the speech from text. Currently, it supports Chinese(zh) and English(en).")
def text_to_speech_generate(text: str, lang: str = "zh"):
  if not os.path.exists(TEMP_CACHE_PATH):
    os.makedirs(TEMP_CACHE_PATH)
  
  out_filename = f"{time.time()}_ning.wav"
  output_path = os.path.join(TEMP_CACHE_PATH, out_filename)
  try:
    dl_models["tts"].forward(input_text=text, lang=lang, output_path=output_path)
  except Exception as e:
    msg = "oops! what had just happened?!"
    logger.error(f"{msg}")
    logger.error(f"{e}")
    raise HTTPException(status_code=500, detail= f"{msg}\nHere is the the error message from the server for you to tell the admin!!!\n{e}")
  return FileResponse(path=output_path, media_type="audio/wav", filename=out_filename)

@app.post("/recognize_speech", summary="Speech to Text Engine", description="Recognize the speech from an audio file. Currently, it supports Chinese(zh) and English(en).")
def speech_to_text_recognize(file: UploadFile = File(...), lang: str="zh"):
  if not os.path.exists(TEMP_CACHE_PATH):
    os.makedirs(TEMP_CACHE_PATH)
  ret, val = save_audio_file(file=file)# return file_name when successfully save the audio files
  if not ret:
    return { "text":"", "msg": val }
  try:
    res = dl_models["stt"].forward(val, lang=lang)
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
  score = dl_models["cer"]([ground_truth], [answer], lang)
  return { "msg": "Success!", "score": score}

@app.post("/do_speech_training", summary="Speech Training Engine", description="Automatically score your audio speech file. Currently, it supports Chinese(zh) and English(en).")
def speech_training(text: str, file: UploadFile = File(...), lang: str="zh"):
  if not os.path.exists(TEMP_CACHE_PATH):
    os.makedirs(TEMP_CACHE_PATH)
  ret, val = save_audio_file(file=file)# return file_name when successfully save the audio files
  if not ret:
    return { "text":"", "msg": val }
  try:
    res = dl_models["stt"].forward(val, lang=lang)
    score = dl_models["cer"]([text], res, lang)
  except Exception as e:
    msg = "oops! what had just happened?!"
    logger.error(f"{msg}")
    logger.error(f"{e}")
    return { "text":"", "msg": f"{msg}\nHere is the the error message from the server for you to tell the admin!!!\n{e}"}
  return { "msg": "Success!", "score": score, "text": res }

@app.get("/")
async def home(): 
  return { "msg": "The Backend Service of The Speech Trainer" }

if __name__ == "__main__":
  LOG_LEVEL = 'TRACE'
  logger.remove()
  logger.add(sys.stdout, level=LOG_LEVEL)

  uvicorn.run("main:app", reload=False, port=8000, host="0.0.0.0")
