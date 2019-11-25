from bs4 import BeautifulSoup
from .links_collection import LinksCollection


def _handle_image(tag, refs):
    if "src" in tag.attrs and tag.attrs["src"]:
        index = refs.add(tag.attrs["src"])
        alt_text = tag.attrs.get("alt", "no description")
        tag.replace_with(f"[image {index}: {alt_text}][{index}]")


def _handle_link(tag, link, refs):
    if (
            len(tag.get_text()) > 0 and
            "href" in tag.attrs and
            len(tag.attrs["href"]) > 0 and
            tag.href != link
    ):
        index = refs.add(tag.attrs["href"])
        tag.insert_after(f"[{index}]")


def _create_refs_text(refs):
    s = ["Links:\n"]
    for i, r in enumerate(refs):
        s.append(f"[{(i+1)}]: {r}\n")
    s = "".join(s)
    return s


def parse(html, skip_link=None):
    refs = LinksCollection()
    if skip_link is not None:
        refs.add(skip_link)
    soup = BeautifulSoup(html, features="lxml")
    for tag in soup.find_all(name=["img", "a"]):
        if tag.name == 'img':
            _handle_image(tag, refs)
        else:
            _handle_link(tag, skip_link, refs)

    text = soup.get_text() + "\n\n" + _create_refs_text(refs)
    return text
