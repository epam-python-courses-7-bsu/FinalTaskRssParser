import logging as log
import feedparser


def print_news(url: str, item: int):
    for item in rss_get_items(url):
        print(item['title'])
        print(item['pubdate'])
        print(item['link'])
        print(item['guid'])
        print(item['discription'])
        print(item['url'])
        print('---')


def print_news_json(url: str, item: int):
    entries = feedparser.parse(url)['entries'][:limit]
    json = {}
    entries.update(json)
    for entry in json:
        print_news(entry)


if __name__ == '__main__':
    received_args = parser.parse_args()
    link = received_args.URL
    limit = received_args.limit
    if received_args.json:
        print_news_json(link, limit)
    if received_args.loglevel:
        print(log.info)
    print_news(link, limit)
