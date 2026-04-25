import argparse
import os
import sys

from pdf2epub.extractor import extract_text
from pdf2epub.cleaner import fix_persian_text, split_paragraphs
from pdf2epub.epub_builder import create_epub


def parse_args():
    parser = argparse.ArgumentParser(
        description="Convert a Persian PDF to EPUB with RTL support."
    )
    parser.add_argument("pdf_path", nargs="?", default="pdf2epub/input.pdf",
                        help="Path to the source PDF file")
    parser.add_argument("--output", "-o", default="output.epub",
                        help="Output EPUB path")
    parser.add_argument("--ocr", action="store_true",
                        help="Force OCR extraction for scanned pages")
    return parser.parse_args()


def main(args=None):
    args = parse_args() if args is None else args

    if not os.path.isfile(args.pdf_path):
        print(f"Error: PDF file not found: {args.pdf_path}")
        sys.exit(1)

    try:
        raw_text, used_ocr, used_pdfplumber = extract_text(
            args.pdf_path, force_ocr=args.ocr
        )
    except RuntimeError as exc:
        print(f"Error: {exc}")
        print("Install OCR dependencies with: pip install pytesseract pillow")
        sys.exit(1)

    if used_pdfplumber:
        print('--- PDFPlumber TEXT PREVIEW ---')
    elif used_ocr:
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

    create_epub(paragraphs, args.output)
    print(f'Created EPUB: {args.output}')
    print(f'OCR used: {used_ocr}')
    print(f'PDFPlumber used: {used_pdfplumber}')


if __name__ == '__main__':
    main()
