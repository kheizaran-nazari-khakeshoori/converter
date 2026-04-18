import contextlib
import fitz  # PyMuPDF
import io
import os
import sys

try:
    from PIL import Image
    import pytesseract
except ImportError:
    Image = None
    pytesseract = None


@contextlib.contextmanager
def suppress_output():
    old_stdout = os.dup(sys.stdout.fileno())
    old_stderr = os.dup(sys.stderr.fileno())
    with open(os.devnull, 'w') as devnull:
        os.dup2(devnull.fileno(), sys.stdout.fileno())
        os.dup2(devnull.fileno(), sys.stderr.fileno())
        try:
            yield
        finally:
            os.dup2(old_stdout, sys.stdout.fileno())
            os.dup2(old_stderr, sys.stderr.fileno())
            os.close(old_stdout)
            os.close(old_stderr)


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

    with suppress_output():
        pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))

    img_data = pix.tobytes("png")
    img = Image.open(io.BytesIO(img_data))
    return pytesseract.image_to_string(img, lang="fas")


def extract_text(pdf_path, force_ocr=False):
    try:
        with suppress_output():
            doc = fitz.open(pdf_path)
    except Exception as exc:
        raise RuntimeError(f"Failed to open PDF: {exc}") from exc

    full_text = ""
    used_ocr = False

    for page_number, page in enumerate(doc, start=1):
        try:
            if not force_ocr:
                with suppress_output():
                    text = page.get_text()

                if text and text.strip():
                    full_text += text + "\n"
                    continue

            text = ocr_page(page)
            used_ocr = True
            full_text += (text or "") + "\n"

        except Exception as exc:
            print(f"[WARNING] Page {page_number} failed: {exc}")
            continue

    return full_text, used_ocr
