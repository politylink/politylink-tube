## setup

### Python
```
poetry install
```

### FFmpeg
```
brew install ffmpeg
```

### Whisper.cpp
https://github.com/ggerganov/whisper.cpp

```
git clone https://github.com/ggerganov/whisper.cpp.git
cd whisper.cpp
make
bash ./models/download-ggml-model.sh large
```

Add 'WHISPER_ROOT' environment variable.
```
export WHISPER_ROOT=${DIR}
```