# speech_trainer
[![Pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit)](https://pre-commit.com/)

Using recent the speech to text, text to speech technologies, we could build a tool that help human to learn languages.
Learning language without training is impossible. This repository contains an application to recognize speech and generate speech as an example.
Using [whisper](https://github.com/openai/whisper) and [coqui-TTS](https://github.com/coqui-ai/TTS) as the speech to text recognizer and text to speech generator.


## Getting Started
To install just execute the bash script or bat file which is provided in the repository root
```
bash install.sh
install.bat
```
To start just execute the bash script or bat file which is provided in the repository root
```
bash start.sh
start.bat
```

## Pre-Commit Setup

Each time you clone this repository, and after do 
```
pip install -r requirements-dev.txt
```
You must run `pre-commit install` to set up the pre-commit hooks. This step is required only for the initial setup.

To run pre-commit manually:
```sh
pre-commit run --all-files
```