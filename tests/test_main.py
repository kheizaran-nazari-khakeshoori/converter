from pdf2epub.main import parse_args


def test_parse_args_defaults():
    args = parse_args([])
    assert args.output == 'output.epub'
    assert args.ocr is False
    assert args.title == 'Persian Book'
    assert args.author == 'pdf2epub'


def test_parse_args_custom_values():
    args = parse_args(['pdf2epub/silver.pdf', '--output', 'silver.epub', '--ocr', '--title', 'Test Book', '--author', 'Test Author'])
    assert args.pdf_path == 'pdf2epub/silver.pdf'
    assert args.output == 'silver.epub'
    assert args.ocr is True
    assert args.title == 'Test Book'
    assert args.author == 'Test Author'
