import rss_get_items as filters
from collections import defaultdict
from collections import OrderedDict


def split_string_by_lines(input_string: str, word_number: int) -> str:
    input_string = input_string.strip().split()
    result = ''
    for idx in range(len(input_string) // word_number + 1):
        start = idx * word_number
        end = (idx + 1) * word_number
        result += ' '.join(input_string[start: end]) + '\n'
    return result.strip()


def prepare_one_item(item_xml: defaultdict) -> OrderedDict:
    """" Take one rss item as dictionary and make ordered dict
    with title, date, description and media content"""
    title = item_xml['title']
    date = filters.pubdate(item_xml['pubDate'])
    news_link = item_xml['link']
    description = split_string_by_lines(
        filters.description(item_xml['description']),
        10
    )
    media_content = split_string_by_lines(
        ' '.join(item_xml['content']),
        1
    )
    prepared_news = OrderedDict()

    prepared_news["Title:"] = title
    prepared_news["Date:"] = date
    prepared_news["Link: "] = news_link
    prepared_news["Description:\n"] = description
    prepared_news["Media content:\n"] = media_content
    return prepared_news


def print_one_item(news_item: OrderedDict) -> None:
    print("===Wow! News!===")
    for key, value in news_item.items():
        print(key, value)
    print("===End, news!===")


def print_news(items: list, limit: int) -> None:
    """" Take list of rss items and print all this news"""
    for item in items[:limit]:
        item = prepare_one_item(item)
        print_one_item(item)

# link_1 = "https://news.yahoo.com/rss/"
# link_2 = "https://news.tut.by/rss/s~173.rss"
# link_3 = 'https://news.google.com/rss?hl=en-US&gl=US&ceid=US:en'
#
# all_items = filters.get_items(link_1)
# print_news(all_items, 3)
#
# all_items = filters.get_items(link_2)
# print_news(all_items, 3)
#
# all_items = filters.get_items(link_3)
# print_news(all_items, 3)
