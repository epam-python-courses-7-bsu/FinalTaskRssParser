from pprint import pprint

from Log import log_decore


@log_decore
def print_json(list_json):
    for i in list_json:
        pprint(i)


@log_decore
def print_array_of_news(news):
    for i in news:
        print("Title: " + i.title)
        print("Date:  " + i.date)
        print("Link:  " + i.link)
        print("\n" + i.news + '\n')
        print("Links: ")
        for l in i.links:
            print(l + "\n")
