from unicodedata import normalize
from numpy import unicode


TEMPLATE = u"""
<h2 class='title'>{title}</h2>
<a class='link' href='{link}'>{title}</a>
<span class='description'>{summary}</span>
"""


def flatten_unicode_keys(entry_properties):
    """Ensures passing unicode keywords to **kwargs."""
    for key in entry_properties:
        if isinstance(key, unicode):
            value = entry_properties[key]
            del entry_properties[key]
            entry_properties[normalize('NFKD', key).encode('ascii', 'ignore')] = value


def entry_to_html(**kwargs):
    """Formats feedparser entry."""
    flatten_unicode_keys(kwargs)
    return TEMPLATE.format(**kwargs).encode('utf-8')