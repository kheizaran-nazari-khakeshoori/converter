from bidi.algorithm import get_display
from pdf2epub.cleaner import fix_persian_text, remove_control_chars


def test_remove_control_chars():
    assert remove_control_chars('ا\u202Eب\u200Fج') == 'ابج'


def test_fix_persian_text_preserves_text():
    source = 'نیازی به این همه خشونت نیست.'
    output = fix_persian_text(source)
    assert output == get_display(source)
