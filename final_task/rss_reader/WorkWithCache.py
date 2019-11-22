import json

from RssException import RssException
# from Handler import News
from Log import log_decore

'''
pass the dictionary to a function and write to a file json
'''


@log_decore
def write_json_to_cache(entry_dict):
    try:
        load_news = json.load(open("cache.json"))
    except json.JSONDecodeError:
        load_news = []
    except FileNotFoundError:
        load_news = []

    if not [item_news for item_news in load_news if item_news["title"] == entry_dict["title"]]:
        load_news.append(entry_dict)

    with open("cache.json", "w") as cache:
        json.dump(load_news, cache, indent=3)


'''
read from the file and, if the date converges, return a list of these news
'''


def read_from_file(date):
    try:
        entries = json.load(open("cache.json"))
    except json.JSONDecodeError:
        raise RssException("emty File")
    except FileNotFoundError:
        raise RssException("File not found error")
    daily_news = []
    date = str(date)
    for item_entries in entries:
        if item_entries["strDate"] == date:
            daily_news.append(item_entries)
    return daily_news
