import feedparser
#from arg import parsargs, VERSION
from arg import parsargs, VERSION
import clean_output
from bs4 import BeautifulSoup 
import json
from loggs import logg, logg_json
import logging
import sys
from datetime import datetime
from add_to_csv import addcsv, out
from converter import convert_date

def get_sourse(parsed):
    ''' Gets source information '''
    feed = parsed['feed']
    return {
        'link': feed['link'],
        'title': feed['title'],
        'subtitle': feed['subtitle'],
    }

def get_news(parsed, console_args):
    """ Gets entries information """
    articles = []
    entries = parsed['entries']
    if console_args.limit is not None:
        ''' Get right amount from the array '''
        entries = entries[:console_args.limit]
    for entry in entries:
        img = BeautifulSoup(entry.summary, features="html.parser")
        summary = BeautifulSoup(entry.summary, features='html.parser').text
        article_img = img.find('img')['src']
        articles.append({
            'link': entry['link'],
            'title': entry['title'],
            'img': article_img,
            'summary': summary,
            'published': entry['published'],
        })
    return articles

def output(article):
    print("Title: ", 
        clean_output.delete_unnecessary_symbols(article['title']))  #clean_output.print("Date: ", article['published'])
    print("Date: ", article['published'])
    print("Link: ", article['link'])
    print("\nSummary: ", article['summary'])
    print("\nImage: ", article['img'])
    print('\n')

def test_to_add(news_csv, articles):
    for i in articles:
        var = True
        for j in news_csv:
            if i['published'] != j[4]:
                var = True
            else:
                var = False
                break
        if var:
            addcsv(i)

def main():
    console_args = arg.parsargs()
    if console_args.version:
        print("Version: ", VERSION)
    parsed = feedparser.parse(console_args.source)
    feed = get_sourse(parsed)
    articles = get_news(parsed, console_args)
    if console_args.verbose:
        logging.info('Website is working')
        
    print('Feed: ', feed['link'], '\n')

    
    news_csv = out()
    test_to_add(news_csv, articles)

    if console_args.date is not None:
        for news in news_csv:
            if int(convert_date(news[4])) == console_args.date:
                print("Title: ", 
                clean_output.delete_unnecessary_symbols(news[1]))  #clean_output.print("Date: ", article['published'])
                print("Date: ", news[4])
                print("Link: ", news[0])
                print("\nSummary: ", news[3])
                print("\nImage: ", news[2])
                print('\n') 


    for article in articles:
        if console_args.json:
            """ Convert to json """ 
            json_format = json.dumps(article)
            print(json_format, '\n')
            article['title'] = clean_output.delete_unnecessary_symbols(article['title'])
            if console_args.verbose:
                logg_json(json_format)
        else:
            output(article)
            if console_args.verbose: 
                logg(article)


if __name__ == '__main__':
    main()