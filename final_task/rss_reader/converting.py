from unicodedata import normalize
from numpy import unicode


def flatten_unicode_keys(dic):
    '''pass unicode keywords to **kwargs '''
    for key in dic.keys():
        if isinstance(key, unicode):
            value = dic[key]
            del dic[key]
            dic[normalize('NFKD',key).encode('ascii','ignore')] = value


def entry2html(**kwargs):
    """ Format feedparser entry """
    flatten_unicode_keys(kwargs)
    title = kwargs['title']
    link = kwargs['link']
    description = kwargs['description']
    template = u"""
    <h2 class='title'>{title}</h2>
    <a class='link' href='{link}'>{title}</a>
    <span class='description'>{description}</span>
    """
    return template.format(title=title, link=link, description=description).encode('utf-8')