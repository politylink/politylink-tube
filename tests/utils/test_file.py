from pathlib import Path

from mylib.utils.file import FilePathHelper


def test_file_path_helper():
    file_path_helper = FilePathHelper(host='')
    assert file_path_helper.get_transcript_fp(1) == Path('./out/transcript/1/data/transcript.json')