import contextlib
import fitz  # PyMuPDF
import os
import sys

try:
    from PIL import Image
    import pytesseract
except ImportError:
    Image = None
    pytesseract = None


@contextlib.contextmanager
def suppress_stderr():
    fd = sys.stderr.fileno()
    with open(os.devnull, 'w') as devnull:
        old_stderr = os.dup(fd)
        os.dup2(devnull.fileno(), fd)
        try:
            yield
        finally:
            os.dup2(old_stderr, fd)
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

    with suppress_stderr():
        pix = page.get_pixmap(dpi=300)

    mode = "RGBA" if pix.alpha else "RGB"
    img = Image.frombytes(mode, [pix.width, pix.height], pix.samples)
    return pytesseract.image_to_string(img, lang="fas+ara")


def extract_text(pdf_path, force_ocr=False):
    try:
        with suppress_stderr():
            doc = fitz.open(pdf_path)
    except Exception as exc:
        raise RuntimeError(f"Failed to open PDF: {exc}") from exc

    full_text = ""
    used_ocr = False

    for page_number, page in enumerate(doc, start=1):
        if force_ocr:
            text = ocr_page(page)
            used_ocr = True
        else:
            try:
                with suppress_stderr():
                    text = page.get_text()
            except Exception as exc:
                text = None

            if not text or is_scan_like_text(text):
                try:
                    text = ocr_page(page)
                    used_ocr = True
                except RuntimeError:
                    raise
                except Exception as exc:
                    raise RuntimeError(
                        f"OCR failed for page {page_number}: {exc}"
                    ) from exc

        full_text += (text or "") + "\n"

    return full_text, used_ocr
