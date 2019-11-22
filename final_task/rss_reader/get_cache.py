from dominate.tags import div, h2, img, p, link
from contextlib import closing
from datetime import datetime
import dominate
import psycopg2
import base64
import time
import json
import os

from . import logg, converter, news_parser


def dateToStamp(arg_date):
    '''
    1. convert --date into timestamp
    '''
    arg_date = str(arg_date)
    arg_date = time.mktime(datetime.strptime(arg_date, '%Y%m%d').timetuple())
    return arg_date


def getCache(limit, tojson, html_path, pdf_path, color, arg_date):
    '''
    1. connect to database
    2. select from table news with published date equals --date
    3. convert news into html or pdf if there are --tohtml or --topdf arguments
    3. or print news in stdout
    '''
    try:
        with closing(psycopg2.connect(database="postgres",user='postgres',password='rssreader',host='db',port='5432')) as con:
            with con.cursor() as cur:
                cur.execute('''SELECT title, link, image, description FROM news WHERE pub_date_stamp >= %s and pub_date_stamp < %s''',
                            (dateToStamp(arg_date), dateToStamp(int(arg_date) + 1)))

                records = cur.fetchall()
                if (html_path or pdf_path):
                    return createHtmlStructure(records, limit, html_path, pdf_path)
                else:
                    return getNewsFromDB(records, limit, tojson, color)

    except psycopg2.ProgrammingError as e:
        print("psycopg2.ProgrammingError: " + str(e))
        logg.logging.error(str(e))


def getNewsFromDB(records, limit, tojson, color):
    '''
    1. create list for news
    2. collect all cache news from db in list
    '''
    news = list()
    for index, row in enumerate(records):
        if(limit and index == limit):
            break
        if (tojson):
            json_news = {
            'Title: ': row[0],
            'Link: ': row[1],
            }
            if(row[3]):
                json_news['Description'] = row[3]
            news.append(json.dumps(json_news))
        else:
            news.append(color + "\nTitle: " + row[0])
            news.append("\nLink: " + row[1] + '\n')
            if (row[3]):
                news.append("Description: " + row[3] + '\n')
    return news


def createHtmlStructure(records, limit, html_path, pdf_path):
    '''
    1. in loop create html structure
    2. create html document or convert html structure into pdf
    '''
    html_document = dominate.document(title="HTML document")
        
    for index, row in enumerate(records):
        if(limit and index == limit):
            break
        with html_document:
            with div():
                h2("Title: " + row[0])
                p("Link: " + row[1])
                if (row[2]):
                    img(src="data:image/jpg;base64," + base64.b64encode(row[2]).decode('ascii'))
                if (row[3]):
                    p("Description: " + row[3])

    if (html_path):
        return str(html_document)
    elif (pdf_path):
        return converter.intoPDF(html_document, pdf_path)
