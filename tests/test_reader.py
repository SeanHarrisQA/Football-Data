from src.Reader import Reader

def test_reader_init():
    test_reader = Reader("lalalala")
    assert test_reader.filepath == "lalalala"