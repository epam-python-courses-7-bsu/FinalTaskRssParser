import feedparser


def get_dict_from_rss_site(source):
    """Function for getting dict from RSS URL"""
    try:
        dict_from_rss_site = feedparser.parse(source)
        if dict_from_rss_site:
            return dict_from_rss_site
        else: return ConnectionError(f"{source} can't be reached")
    except OSError:
        raise ConnectionError(f"{source} can't be reached")


def check_key_in_dict_from_rss_site(dict_from_rss_site, key):
    """Function for checking existing of key in dict"""
    if dict_from_rss_site.get(key, None):
        return True
    return False


def get_news(source):
    """Function for creation dict news, where key "News" and value is list of news, from RSS URL's news.
    Sourse is RSS URL"""
    dict_from_rss_site = get_dict_from_rss_site(source)
    news = []
    news_reslt = {}
    if check_key_in_dict_from_rss_site(dict_from_rss_site, 'entries'):
        for entry in dict_from_rss_site.entries:
            site_info = {}
            if check_key_in_dict_from_rss_site(dict_from_rss_site, 'feed'):
                if check_key_in_dict_from_rss_site(dict_from_rss_site.feed, 'title'):
                    site_info['Feed'] = dict_from_rss_site.feed.title
            if check_key_in_dict_from_rss_site(entry, 'title'):
                site_info['Title'] = entry.title
            if check_key_in_dict_from_rss_site(entry, 'published'):
                site_info['Date'] = entry.published
            if check_key_in_dict_from_rss_site(entry, 'link'):
                site_info['Link'] = entry.link
            news.append(site_info)
    news_reslt['News'] = news
    if news:
        return news_reslt
    else:
        return f"{source} can't be reached"
