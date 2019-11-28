from urllib.request import Request, urlopen
from datetime import datetime
from colored import stylize
import arg_parser
import feedparser
import requests
import colored
import html
import sys
import os

import logg


def main(version):

    args = arg_parser.createArgparser(version)
    params = dict()

    if (args.verbose):
        logg.makeVerbose()
        requests.get('http://127.0.0.1:5000/verbose/')

    if(args.colorize):
        color = [colored.fg(150), colored.fg(50), colored.fg(189)]
    else:
        color = [colored.attr('reset'), colored.attr('reset'), colored.attr('reset')]

    params = {'limit':args.limit, 'tojson': args.json,
    'tohtml':args.tohtml, 'topdf':args.topdf, 'color':color}

    if (args.date):
        params['date'] = args.date
        r = requests.get('http://127.0.0.1:5000/getcache/', json=params)
        news = r.text

        if(args.tohtml):
            saveHTML(news, args.tohtml)
        elif(args.topdf):
            pdf_document = bytes(news, 'utf-8')
            savePDF(pdf_document, args.topdf)
        else:
            print(news)
    else:
        try:
            checkConnection(args.source)
            params['url'] = args.source
            r = requests.get('http://127.0.0.1:5000/print/', json=params)
            news = r.text

            if(args.tohtml):
                saveHTML(news, args.tohtml)
            elif(args.topdf):
                pdf_document = bytes(news, 'utf-8')
                savePDF(pdf_document, args.topdf)
            else:
                print(news)
        except Exception as e:
            logg.logging.error("Connection error" + str(e))
            print("Connection error: ", e)



def saveHTML(html_document, html_path):
    '''
    1. create folder with html file
    2. write html structure in file
    '''
    if not os.path.exists(html_path):
        os.makedirs(html_path)
    time_name = datetime.strftime(datetime.now(), "%H%M%S")
    file_name = 'NewsFeed' + '-' + time_name + '.html'
    html_file = os.path.join(html_path, file_name)

    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(str(html_document))


def savePDF(doc, pdf_path):
    '''
    1. create folder with pdf file
    2. write pdf in file
    '''
    if not os.path.exists(pdf_path):
        os.makedirs(pdf_path)
    time_name = datetime.strftime(datetime.now(), "%H%M%S")
    file_name = 'NewsFeed' + '-' + time_name + '.pdf'
    pdf_file = os.path.join(pdf_path, file_name)

    with open(pdf_file, "w+b") as resultFile:
        resultFile.write(doc)


def checkConnection(source):
    '''Check connection to server'''
    try:
        source = Request(source)
        response = urlopen(source)
    except Exception as e:
        raise Exception(e)
    else:
        logg.logging.info('Website is working')


if __name__ == "__main__":
    # Check connection to server
    try:
        version = (requests.get('http://127.0.0.1:5000/version/')).text
        main(version)
    except requests.exceptions.ConnectionError as error:
        print("ConnectionError: " + str(error))
        logg.logging.error("ConnectionError: " + str(error))
