from pathlib import Path

from mylib.utils.constants import ImageSize
from mylib.utils.path import PathHelper


def test_path_helper_local():
    path_helper = PathHelper()
    assert path_helper.get_transcript_fp(1) == Path("./out/transcript/1/data/transcript.csv")
    assert path_helper.get_local_clip_image_fp(1, ImageSize.MEDIUM) == Path("./out/artifact/image/clip/m/1.jpg")
    assert path_helper.to_s3_image_fp(Path("./out/artifact/image/clip/m/1.jpg")) == Path("player/clip/m/1.jpg")


def test_path_helper_host():
    path_helper = PathHelper(host="mini")
    assert path_helper.get_transcript_fp(1) == Path("./out_mini/transcript/1/data/transcript.csv")
