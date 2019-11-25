import json
import os

from RssException import RssException
# from Handler import News
from Log import log_decore
import urllib.request

'''
pass the dictionary to a function and write to a file json
'''


@log_decore
def correct_title(title):
    return title.replace('"', "_").replace("?", "_").replace(":", "_").replace("'", "_").replace(" ", "_")[:15]


@log_decore
def save_img(url, name):
    if os.path.exists("images"):
        if name.find(".jpg") == -1:
            urllib.request.urlretrieve(url, f'images/{name}.jpg')
        else:
            urllib.request.urlretrieve(url, f'images/{name}')
    else:
        os.makedirs("images")
        urllib.request.urlretrieve(url, f"images/{name}.jpg")


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
        if(entry_dict["links"][0] != ''):
            save_img(entry_dict["links"][0], correct_title(entry_dict["title"]))

    with open("cache.json", "w") as cache:
        json.dump(load_news, cache, indent=3)



'''
read from the file and, if the date converges, return a list of these news
'''


def read_from_file(date, lim):
    # here we look, if = -1, then we make a flag to read all the news
    flag = 0
    if lim == -1:
        flag = 1
    try:
        entries = json.load(open("cache.json"))
    except json.JSONDecodeError:
        raise RssException("emty File")
    except FileNotFoundError:
        raise RssException("File not found error")
    daily_news = []
    date = str(date)
    for item_entries in entries:
        if item_entries["strDate"] == date and (lim or flag):
            daily_news.append(item_entries)
            lim -= 1
    return daily_news
