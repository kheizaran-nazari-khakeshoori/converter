# pdf2epub

A small Python project that extracts Persian text from PDF files and generates an RTL EPUB.

## What this repository provides

- A Python package in `pdf2epub/`
- A converter script at `pdf2epub/main.py`
- Persian text cleanup with hidden-control-character removal and bidi display
- EPUB creation with proper RTL HTML metadata

## Install

Use the package requirements:

```bash
python -m pip install -r pdf2epub/requirements.txt
```

Or install locally as a package:

```bash
python -m pip install .
```

## Usage

Convert a PDF to EPUB:

```bash
python -m pdf2epub.main pdf2epub/silver.pdf --output output.epub
```

To force OCR for scanned PDFs:

```bash
python -m pdf2epub.main pdf2epub/silver.pdf --ocr --output output.epub
```

## Notes

- `pdf2epub/silver.pdf` is a sample source file in this repository.
- If your PDF is scanned, install Tesseract with `sudo apt install tesseract-ocr tesseract-ocr-fas`.

## Testing

Run tests with:

```bash
python -m pytest
```
