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


### Sync
```
rsync -a -v --exclude '*.wav' --exclude '*.mp3' --exclude '*.mp4' mitsuki@intel:~/politylink/politylink-press/out ./out/intel
rsync -a -v --exclude '*.wav' --exclude '*.mp3' --exclude '*.mp4' ./out/intel/out mitsuki@mini:~/politylink/politylink-press/out/intel
scp mitsuki@intel:~/politylink/politylink-press/db/local.db ./db/intel.db
scp ./db/intel.db mitsuki@mini:~/politylink/politylink-press/db/intel.db
tar -zcvf artifact.tar.gz artifact
scp mitsuki@mini:~/politylink/politylink-press/out/artifact.tar.gz ./out/
tar -xvf artifact.tar.gz
```