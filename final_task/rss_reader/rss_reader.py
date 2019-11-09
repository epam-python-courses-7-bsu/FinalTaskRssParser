import feedparser
from pprint import pprint
from myargparse import parsargs
from bs4 import BeautifulSoup 
import json

args = parsargs()

parsed = feedparser.parse(args.source)

def get_sourse(parsed):
    ''' Gets source information '''
    feed = parsed['feed']
    return {
        'link': feed['link'],
        'title': feed['title'],
        'subtitle': feed['subtitle'],
    }

def get_news(parsed):
    """ Gets entries information """
    articles = []
    entries = parsed['entries']
    entries = entries[:args.limit] # Get the right amount from the array
    for entry in entries:
        soup = BeautifulSoup(entry['summary'], 'lxml')
        article_img = soup.find('img')['src']
        articles.append({
            'link': entry['link'],
            'title': entry['title'],
            'img': article_img,
            'summary': entry['summary'],
            'published': entry['published'],
        })
    return articles

def to_json(articles):
    """ Convert to json """ 
    return json.dumps(articles)

def output(articles):
    print("Title: ", value['title'])
    print("Date: ", value['published'])
    print("Link: ", value['link'])
    print("\nSummary: ", value['summary'])
    print("\nImage: ", value['img'])
    print('\n')

if __name__ == '__main__':
    feed = get_sourse(parsed)
    articles = get_news(parsed)
    print('Feed: ', feed['link'], '\n')
    if args.json:
        for value in articles:
            j = to_json(articles)
            print(j, '\n')
    else:
        for value in articles:
            output(articles)

