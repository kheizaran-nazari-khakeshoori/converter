import re


def fix_persian_text(text):
    if not text:
        return text

    fixed_lines = []
    for line in text.splitlines(keepends=True):
        tokens = re.findall(r'\s+|\S+', line)
        words = [t for t in tokens if not t.isspace()]
        if len(words) < 2:
            fixed_lines.append(line)
            continue

        reversed_words = list(reversed(words))
        fixed_line = []
        word_index = 0
        for token in tokens:
            if token.isspace():
                fixed_line.append(token)
            else:
                fixed_line.append(reversed_words[word_index])
                word_index += 1

        fixed_lines.append(''.join(fixed_line))

    return ''.join(fixed_lines)


def split_paragraphs(text):
    paragraphs = text.split("\n\n")
    return [p.strip() for p in paragraphs if p.strip()]
