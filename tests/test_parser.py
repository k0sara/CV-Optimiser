import pytest

from src.parser import UnsupportedFileType, parse_document


def test_parse_text():
    result = parse_document(b"hello world", "cv.txt")
    assert result.text == "hello world"
    assert result.file_type == "txt"


def test_reject_unknown_file_type():
    with pytest.raises(UnsupportedFileType):
        parse_document(b"data", "cv.pages")

