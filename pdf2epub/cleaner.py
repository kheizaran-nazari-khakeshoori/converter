import arabic_reshaper
from bidi.algorithm import get_display


def fix_persian_text(text):
    if not text:
        return text

    fixed_lines = []
    for line in text.splitlines(keepends=True):
        reshaped = arabic_reshaper.reshape(line)
        bidi_text = get_display(reshaped)
        fixed_lines.append(bidi_text)

    return "".join(fixed_lines)


def split_paragraphs(text):
    paragraphs = text.split("\n\n")
    return [p.strip() for p in paragraphs if p.strip()]
