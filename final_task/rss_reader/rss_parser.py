from builtins import set

from bs4 import BeautifulSoup as bs
from urllib.request import urlopen
from test import urls


def main():
    html = urlopen(urls[0])
    bsObj = bs(html, features="html.parser")

    # print(bsObj.find_all('title'))
    site = bsObj.find('item')
    date = set(bsObj.find('pubdate'))

    for items in site:
        for dates in date:
            print(items)
            # print(dates)


if __name__ == '__main__':
    main()
