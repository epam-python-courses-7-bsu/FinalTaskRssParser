import feedparser
from pprint import pprint
from arg import parsargs, vers
from clean_output import delete_html, clean
from bs4 import BeautifulSoup 
import json
from loggs import logg, logg_json
import logging

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
    if args.limit is not None:
        ''' Get right amount from the array '''
        entries = entries[:args.limit]
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

def output(value):
    print("Title: ", clean(value['title']))
    print("Date: ", value['published'])
    print("Link: ", value['link'])
    print("\nSummary: ", clean(delete_html(value['summary'])))
    print("\nImage: ", value['img'])
    print('\n')

if __name__ == '__main__':
    feed = get_sourse(parsed)
    articles = get_news(parsed)
    if args.verbose:
        logging.info('Website is working')
        
    print('Feed: ', feed['link'], '\n')

    for value in articles:
        if args.json:
            """ Convert to json """ 
            json_format = json.dumps(value)
            print(json_format, '\n')
            if args.verbose:
                logg_json(json_format)
        else:
            output(value)
            if args.verbose: 
                logg(value)
        
    if args.version:
        print("Version: ",vers)
