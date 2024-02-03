import os
import time
from pydub import AudioSegment
from loguru import logger

def save_audio_file(file):
  file_name = f"{time.time()}_{file.filename}"
  file_name = os.path.join("temp_cache", file_name)
  pre, ext = os.path.splitext(file_name)
  if ext == "":
    file_name = f"{file_name}.wav"
  try:
    contents = file.file.read()
    with open(file_name, 'wb') as f:
      f.write(contents)
    if ext != ".wav":
      ext = ext.replace('.', '')
      sound = AudioSegment.from_file(file_name, format=ext)
      file_name = f"{pre}.wav"
      file_handle = sound.export(file_name, format='wav')
  except Exception as e:
    msg = "oops!! There was an error uploading the file"
    logger.error(f"{msg}")
    logger.error(f"{e}")
    return False, f"{msg}\nHere is the the error message from the server for the admin!!!\n{e}"
  return True, file_name