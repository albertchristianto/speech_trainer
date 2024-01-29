from fastapi import File, UploadFile, Form, FastAPI, APIRouter, HTTPException
from fastapi.responses import FileResponse
from typing import Optional

from loguru import logger

# from models.stt import Speech2Text
# from models.tts import Text2Speech

app = FastAPI()

@app.get("/generate_sample_audio")
def text_to_speech_generate():
  return { "msg": "Not yet implemented!" }

@app.post("/recognize_speech")
def speech_to_text_recognize():
  return { "msg": "Not yet implemented!" }

@app.get("/get_score")
def text_to_speech_generate():
  return { "msg": "Not yet implemented!" }

@app.get("/")
async def home(): 
  return { "msg": "The Backend Service of The Speech Trainer" }