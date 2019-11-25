from pprint import pprint

from Log import log_decore


@log_decore
def print_json(list_json):
    for item_list in list_json:
        pprint(item_list)


@log_decore
def print_array_of_news(news):
    for item_news in news:
        print("Title: " + item_news.title)
        print("Date:  " + item_news.date)
        print("Link:  " + item_news.link)
        print("\n" + item_news.news + '\n')
        print("Links: ")
        for item_link in item_news.links:
            print(item_link + "\n")


@log_decore
def print_array_of_dict(news):
    for item_news in news:
        print("Title: " + item_news["title"])
        print("Date:  " + item_news["date"])
        print("Link:  " + item_news["link"])
        print("\n" + item_news["news"] + '\n')
        print("Links: ")
        for item_link in item_news["links"]:
            print(item_link + "\n")
