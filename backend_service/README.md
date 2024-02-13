# Getting Started
Requirement:
1. Python 3.10, preferably using Anaconda (for windows)
2. CUDA 11.8 (could be changed to CUDA 12.1)
3. C++ Desktop Development(for windows)

To install the backend service, follow this step:

For Windows, you need to execute this environment setup for the C++ compiler before execute install.bat
```
"C:/Program Files/Microsoft Visual Studio/2022/Community/VC/Auxiliary/Build/vcvars64.bat"
install.bat # for windows
install.sh # for linux
```
Download the weights for stt and tts from these links:
1. https://huggingface.co/openai/whisper-small/tree/main 
2. https://huggingface.co/coqui/XTTS-v2/tree/main

Put the data into "backend_service/weights/whisper-small" and "backend_service/weights/xttsv2"

And, execute the backend service server with 
```
# then execute the backend service server
python main.py
```

## API Documentation
The backend service is built using FastAPI framework where the documentations of the HTTP APIs are generated automatically and can be accessed in http://localhost:8000/docs

## Reference Repository
1. https://github.com/zszyellow/WER-in-python/tree/master 
2. https://github.com/speechio/chinese_text_normalization/tree/master 
3. https://huggingface.co/datasets/mozilla-foundation/common_voice_11_0 