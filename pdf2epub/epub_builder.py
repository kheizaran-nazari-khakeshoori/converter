from ebooklib import epub


def create_epub(paragraphs, output_path):
    book = epub.EpubBook()

    book.set_title("Persian Book")
    book.set_language("fa")

    content = ""
    for p in paragraphs:
        content += f"<p>{p}</p>"

    chapter = epub.EpubHtml(
        title="Chapter 1",
        file_name="chap1.xhtml",
        lang="fa"
    )

    chapter.content = f"""
    <html dir="rtl">
    <body>
    {content}
    </body>
    </html>
    """

    book.add_item(chapter)
    book.spine = ['nav', chapter]

    epub.write_epub(output_path, book)
