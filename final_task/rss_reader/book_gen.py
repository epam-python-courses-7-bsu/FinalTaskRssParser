import time
import os.path
import html

from ebooklib import epub

DATE_FORMAT = "%Y%m%d"


def _render_document(title, items, date_str):
    html = ["<html><head><title>"]
    h_title = f"{date_str}"
    html.append(h_title)
    html.append("</title></head><body>")

    html.append("<h1>")
    html.append(title)
    html.append("</h1>")

    for i in items:
        html.append(_render_item(i))

    html = "".join(html)
    return html


def _render_item(item):
    html = ["<hr>"]
    title = item["title"] or "No Headline"
    html.append(f"<h2>{title}</h2>")
    date = time.strftime("%a, %d %b %Y %H:%M:%S", item["date"])
    html.append(f"<p><i>{date}</i></p>")
    if item["link"] is not None:
        link = item["link"]
        html.append(f"<p><a href='{link}'>{link}</a></p>")
    else:
        html.append(f"<p><a>no link</a></p>")
    description = item["description"] or "No description"
    html.append(f"<p>{description}</p>")
    html = "".join(html)
    return html


def _gen_id(title: str, date:str) -> str:
    """
    generate string for book id and file name

    :return: generated string
    """
    string = title + "_" + date
    string = string.lower()
    for c in r'\|/:*?"<>':
        string.replace(c, '_')
    if len(string) > 122:
        string = string[:121] + "..."
    return string


def _create_html(book_id, bookpath, text):
    # text = html.escape(text)
    file = None
    if os.path.isdir(bookpath):
        file = open(os.path.join(bookpath, book_id + ".html"), "w", encoding="utf-8")
    elif not os.path.exists(bookpath) or os.path.isfile(bookpath) or os.path.islink(bookpath):
        file = open(bookpath, "w", encoding="utf-8")
    try:
        file.write(text)
        file.close()
    except (AttributeError, OSError):
        pass


def _create_epub(book_title, book_id, bookpath, text):

    book = epub.EpubBook()
    book.set_language('en')
    book.set_identifier(book_id)
    book.set_title(book_title)

    content = epub.EpubHtml(title='News', file_name='content.xhtml')

    content.set_content(text)
    book.add_item(content)

    book.toc = (content,)
    book.spine = [content]
    book.add_item(epub.EpubNcx())
    book.add_item(epub.EpubNav())
    if os.path.isdir(bookpath):
        epub.write_epub(os.path.join(bookpath, book_id+".epub"), book)
    elif not os.path.exists(bookpath) or os.path.isfile(bookpath) or os.path.islink(bookpath):
        epub.write_epub(bookpath, book)


def create_book(title, items, bookpath, date=None, *, html=False):
    if date is not None:
        date = time.strftime(DATE_FORMAT, date)
    else:
        date = "Latest"

    if title is None:
        title = "No Title"
    book_title = title + " - " + date
    text = _render_document(book_title, items, date)
    book_id = _gen_id(title, date)

    if html:
        _create_html(book_id, bookpath, text)
    else:
        _create_epub(book_title, book_id, bookpath, text)
