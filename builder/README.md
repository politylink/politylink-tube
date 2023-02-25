# 概要
このディレクトリにはPolityLinkのサイト用のデータ（会議情報・文字起こしなど）を生成するコードが置かれています。
builderが生成したJSONデータ（artifactと呼びます）は、frontendのビルド時に参照されます。

# 環境構築
記載のコードはMacOSに環境構築する場合です。適宜読み替えて実行してください。

## Python
builderの実行にはPython >= 3.10が必要です。[Pyenv](https://github.com/pyenv/pyenv)などのツールでインストールしてください。

```
brew install pyenv
```

```
pyenv install 3.10.4
```

Pythonのパッケージ管理には[Poetry](https://python-poetry.org/docs/)を使っています。
```
curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python
```

```
poetry env use 3.10
poetry install
poetry shell
```
`install`コマンドで必要なパッケージが入った仮想環境が構築され、`poetry shell`もしくは`poetry run ${command}`で仮想環境内でコードを実行できます。  


## ツール
音声ファイルの取得や文字起こしの生成は、各種ツールを使って実行しています。それぞれインストールしてパスを通してください。

### FFmpeg
FFmpegは音声ファイルのダウンロードやフォーマット変換に使います。

```
brew install ffmpeg
```

### Whisper.cpp
[Whisper.cpp](https://github.com/ggerganov/whisper.cpp)はOpenAIが公開した文字起こしモデルWhisperを、CPU環境でも高速に実行できるように最適化したツールです。音声ファイルから文字起こしを生成する際に使います。

```
git clone https://github.com/ggerganov/whisper.cpp.git
cd whisper.cpp
make
bash ./models/download-ggml-model.sh large
```

Pythonから呼び出せるように、インストールしたディレクトリを`WHISPER_ROOT`という環境変数に登録する必要があります。
以下のコードを`.zshenv`などに記載してください。
```
export WHISPER_ROOT=${YOUR_INSTALL_DIR}
```

### SQLite
動画のメタデータなどはSQliteを使って管理しています。MacOSの場合デフォルトでインストールされています。
