import fitz  # PyMuPDF

try:
    from PIL import Image
    import pytesseract
except ImportError:
    Image = None
    pytesseract = None


def is_scan_like_text(text):
    if not text or text.strip() == "":
        return True

    lower = text.lower()
    if lower.count("camscanner") > 5:
        return True

    words = [w for w in text.split() if w.isalpha()]
    if len(words) < 5 and len(text) < 150:
        return True

    return False


def ocr_page(page):
    if Image is None or pytesseract is None:
        raise RuntimeError(
            "OCR dependencies are not installed. Install pytesseract and pillow to use OCR."
        )

    pix = page.get_pixmap(dpi=300)
    mode = "RGBA" if pix.alpha else "RGB"
    img = Image.frombytes(mode, [pix.width, pix.height], pix.samples)
    return pytesseract.image_to_string(img, lang="fas+ara")


def extract_text(pdf_path, force_ocr=False):
    doc = fitz.open(pdf_path)
    full_text = ""
    used_ocr = False

    for page in doc:
        if force_ocr:
            text = ocr_page(page)
            used_ocr = True
        else:
            text = page.get_text()
            if is_scan_like_text(text):
                text = ocr_page(page)
                used_ocr = True

        full_text += text + "\n"

    return full_text, used_ocr
