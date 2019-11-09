import feedparser


def parse(url):
    return feedparser.parse(url)

def get_sourse(parsed):
    ''' Gets source information '''
    feed = parsed['feed']
    return {
        'link': feed['link'],
        'title': feed['title'],
        'subtitle': feed['subtitle'],
    }

if __name__ == '__main__':
    parsed = parse("https://news.yahoo.com/rss/")
    feed = get_sourse(parsed)
    print('Feed: ', feed['link'], '\n')
