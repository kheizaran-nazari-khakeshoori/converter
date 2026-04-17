from extractor import extract_text
from cleaner import fix_persian_text, split_paragraphs
from epub_builder import create_epub


if __name__ == '__main__':
    pdf_path = 'input.pdf'
    output_path = 'output.epub'

    raw_text = extract_text(pdf_path)
    print('--- RAW TEXT PREVIEW ---')
    print(raw_text[:1000])
    print('--- END RAW TEXT PREVIEW ---\n')

    clean_text = fix_persian_text(raw_text)
    paragraphs = split_paragraphs(clean_text)

    print('--- CLEAN PREVIEW ---')
    for p in paragraphs[:5]:
        print(p)
        print('----')

    create_epub(paragraphs, output_path)
    print(f'Created EPUB: {output_path}')
