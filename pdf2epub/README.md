# pdf2epub

A small Python project to extract Persian text from PDFs and build an EPUB.

## What it does

- extracts text from `input.pdf` using PyMuPDF
- reshapes Persian/Arabic letters and applies bidi ordering
- splits text into paragraphs
- writes a simple RTL EPUB

## Requirements

Install dependencies with:

```bash
pip install -r requirements.txt
```

Optional OCR support:

```bash
pip install pytesseract pillow
```

## Usage

Place `input.pdf` inside the `pdf2epub` folder, then run:

```bash
python pdf2epub/main.py
```

## Limitations

- only works for text PDFs, not scanned images
- simple paragraph splitting by blank lines
- produces a single-chapter EPUB with basic formatting
- RTL layout may still need manual review
