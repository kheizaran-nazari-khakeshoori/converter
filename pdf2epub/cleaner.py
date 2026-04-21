import re
from bidi.algorithm import get_display


def remove_control_chars(text):
    return re.sub(r'[\u202A-\u202E\u200E\u200F]', '', text)


def fix_persian_text(text):
    if not text:
        return text

    text = remove_control_chars(text)
    return get_display(text)


def split_paragraphs(text):
    paragraphs = text.split("\n\n")
    return [p.strip() for p in paragraphs if p.strip()]
