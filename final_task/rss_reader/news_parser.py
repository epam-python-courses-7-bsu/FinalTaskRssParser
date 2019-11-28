from email.utils import parsedate_to_datetime
from contextlib import closing
from bs4 import BeautifulSoup
from datetime import datetime
import requests
import sqlite3
import psycopg2
import json
import time
import html
import os

from . import logg
from . import config


def checkMediaContent(item):
    '''check if there is media content'''
    media_content = ''
    if ('media_content' in item.keys()):
        media_content = item.media_content[0]['url']
    elif ('media_thumbnail' in item.keys()):
        media_content = item.media_thumbnail[0]['url']
    return media_content


def getDescription(description):
    '''return description without html tags'''
    return BeautifulSoup(description, features="html.parser").getText()


def intoJson(item):
    '''print news in json format'''
    json_news = {
        'Title: ': html.unescape(item.title),
        'Date: ': item.published,
        'Link: ': item.link
        }
    description = getDescription(item.description)
    media_link = checkMediaContent(item)
    if(description):
        json_news['Description: '] = description
    if(media_link):
        json_news['Media link: '] = media_link
    return json.dumps(json_news)


def cacheNews(channel):
    '''
    1. connect to database
    2. create table in database
    3. insert news into table
    '''
    con = None
    try:
        params = config.config()

        with psycopg2.connect(**params) as con:
            with con.cursor() as cur:
                cur.execute("""CREATE TABLE IF NOT EXISTS news
                                (title text, link text, image bytea,
                                description text, pub_date_stamp real,
                                UNIQUE (title, link, pub_date_stamp))
                                """)

                news = insertNewsIntoTable(channel)
                cur.executemany("INSERT INTO news VALUES (%s,%s,%s,%s,%s) ON CONFLICT DO NOTHING", news)
                con.commit()
                logg.logging.info("News cached into database")

    except (Exception, psycopg2.DatabaseError) as e:
        logg.logging.error(str(e))
    finally:
        if con is not None:
            con.close()
            logg.logging.info("Database connection closed")


def insertNewsIntoTable(channel):
    '''
    1. fill table with news
    2. convert date into timestamp
    '''
    news = list()

    for index, item in enumerate(channel.entries):

        description = getDescription(item.description)

        try:
            pub_date_stamp = time.mktime(parsedate_to_datetime(item.published).timetuple())
        except ValueError as error:
            logg.logging.error("ValueError: " + str(error))
        
        media_content = checkMediaContent(item)
        image = ''

        if (media_content):
            try:
                response = requests.get(media_content)
                image = psycopg2.Binary(response.content)
            except Exception as error:
                logg.logging.error("Exception: " + str(e))

        row = (html.unescape(item.title), item.link, image, description, pub_date_stamp)
        news.append(row)
    return news

