import contextlib
import fitz  # PyMuPDF
import io
import os
import shutil
import subprocess
import sys
import tempfile

try:
    from PIL import Image
    import pytesseract
except ImportError:
    Image = None
    pytesseract = None

try:
    import pdfplumber
except ImportError:
    pdfplumber = None


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


def render_page_with_pdftoppm(pdf_path, page_number):
    if not shutil.which('pdftoppm'):
        raise RuntimeError('pdftoppm is not installed. Install poppler-utils to use this fallback.')

    with tempfile.TemporaryDirectory() as tmpdir:
        out_prefix = os.path.join(tmpdir, 'page')
        cmd = [
            'pdftoppm',
            '-f', str(page_number),
            '-l', str(page_number),
            '-png',
            '-r', '300',
            pdf_path,
            out_prefix,
        ]
        with suppress_output():
            subprocess.run(cmd, check=True)

        png_path = f"{out_prefix}-{page_number}.png"
        if not os.path.exists(png_path):
            raise RuntimeError(f'pdftoppm did not produce output for page {page_number}')

        with open(png_path, 'rb') as f:
            return Image.open(io.BytesIO(f.read())).convert('L')


def ocr_page(page, pdf_path=None, page_number=None):
    if Image is None or pytesseract is None:
        raise RuntimeError(
            "OCR dependencies are not installed. Install pytesseract and pillow to use OCR."
        )

    text = ""
    img = None
    try:
        with suppress_output():
            pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))

        img_data = pix.tobytes('png')
        img = Image.open(io.BytesIO(img_data)).convert('L')
        text = pytesseract.image_to_string(img, lang='fas', config='--psm 6')
    except Exception:
        pass

    if not text.strip() and pdf_path is not None and page_number is not None:
        try:
            img = render_page_with_pdftoppm(pdf_path, page_number)
            text = pytesseract.image_to_string(img, lang='fas', config='--psm 6')
            if not text.strip():
                text = pytesseract.image_to_string(img, config='--psm 6')
        except Exception:
            pass

    if text is None:
        text = ""

    return text


def extract_with_pdfplumber(pdf_path):
    if pdfplumber is None:
        raise RuntimeError(
            "pdfplumber is not installed. Install it with pip install pdfplumber."
        )

    full_text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page_number, page in enumerate(pdf.pages, start=1):
            try:
                page_text = page.extract_text() or ""
            except Exception:
                page_text = ""
            full_text += page_text + "\n"

    return full_text


def extract_text(pdf_path, force_ocr=False):
    try:
        with suppress_output():
            doc = fitz.open(pdf_path)
    except Exception as exc:
        raise RuntimeError(f"Failed to open PDF: {exc}") from exc

    full_text = ""
    used_ocr = False
    used_pdfplumber = False

    for page_number, page in enumerate(doc, start=1):
        try:
            if not force_ocr:
                with suppress_output():
                    text = page.get_text()

                if text and text.strip():
                    full_text += text + "\n"
                    continue

            text = ocr_page(page, pdf_path=pdf_path, page_number=page_number)
            used_ocr = True
            full_text += (text or "") + "\n"

        except Exception as exc:
            print(f"[WARNING] Page {page_number} failed: {exc}")
            continue

    if not full_text.strip() and not force_ocr and pdfplumber is not None:
        try:
            full_text = extract_with_pdfplumber(pdf_path)
            if full_text.strip():
                used_pdfplumber = True
        except Exception:
            pass

    return full_text, used_ocr, used_pdfplumber
