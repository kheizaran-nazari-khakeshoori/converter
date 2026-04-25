import os
import tempfile

from pdf2epub.epub_builder import create_epub


def test_create_epub_creates_file():
    with tempfile.TemporaryDirectory() as tmp:
        output_path = os.path.join(tmp, 'test.epub')
        create_epub(['سلام دنیا'], output_path)
        assert os.path.exists(output_path)
