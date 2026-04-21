import re


def fix_persian_text(text):
    if not text:
        return text

    tokens = re.findall(r'\S+|\s+', text)
    fixed = []
    for token in tokens:
        if token.isspace():
            fixed.append(token)
        else:
            fixed.append(token[::-1])
    return ''.join(fixed)


def split_paragraphs(text):
    paragraphs = text.split("\n\n")
    return [p.strip() for p in paragraphs if p.strip()]
