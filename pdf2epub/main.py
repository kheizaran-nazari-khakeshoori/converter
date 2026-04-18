import os
import sys

from extractor import extract_text
from cleaner import fix_persian_text, split_paragraphs
from epub_builder import create_epub


if __name__ == '__main__':
    args = sys.argv[1:]
    force_ocr = False

    if '--ocr' in args:
        force_ocr = True
        args.remove('--ocr')

    pdf_path = args[0] if args else 'input.pdf'
    output_path = 'output.epub'

    if not os.path.isfile(pdf_path):
        print(f"Error: PDF file not found: {pdf_path}")
        print("Place your PDF at pdf2epub/input.pdf or pass a path as an argument.")
        sys.exit(1)

    try:
        raw_text, used_ocr = extract_text(pdf_path, force_ocr=force_ocr)
    except RuntimeError as exc:
        print(f"Error: {exc}")
        print("Install OCR dependencies with: pip install pytesseract pillow")
        sys.exit(1)

    if used_ocr:
        print('--- OCR TEXT PREVIEW ---')
    else:
        print('--- RAW TEXT PREVIEW ---')

    print(raw_text[:1000])
    print('--- END TEXT PREVIEW ---\n')

    clean_text = fix_persian_text(raw_text)
    paragraphs = split_paragraphs(clean_text)

    print('--- CLEAN PREVIEW ---')
    for p in paragraphs[:5]:
        print(p)
        print('----')

    create_epub(paragraphs, output_path)
    print(f'Created EPUB: {output_path}')
