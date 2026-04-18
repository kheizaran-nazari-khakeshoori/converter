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

For scanned PDFs, install Tesseract OCR support as well:

```bash
sudo apt install tesseract-ocr tesseract-ocr-fas
```

## Usage

Place `input.pdf` inside the `pdf2epub` folder, then run:

```bash
python pdf2epub/main.py
```

To force OCR explicitly:

```bash
python pdf2epub/main.py input.pdf --ocr
```

If your PDF is a scanned image, the script will now fallback to OCR automatically.

## Limitations

- only works for text PDFs, not scanned images
- simple paragraph splitting by blank lines
- produces a single-chapter EPUB with basic formatting
- RTL layout may still need manual review
