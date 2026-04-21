import re


def fix_persian_text(text):
    if not text:
        return text

    fixed_lines = []
    for line in text.splitlines(keepends=True):
        parts = re.split(r'(\s+)', line)
        fixed_line = ""

        for part in parts:
            if part.isspace():
                fixed_line += part
            else:
                fixed_line += part[::-1]

        fixed_lines.append(fixed_line)

    return "".join(fixed_lines)


def split_paragraphs(text):
    paragraphs = text.split("\n\n")
    return [p.strip() for p in paragraphs if p.strip()]
