import datetime
from contextlib import closing

import psycopg2
import News
import os
import logging

MODULE_LOGGER = logging.getLogger("rss_reader.database")


def get_param_for_connect(filename) -> dict:
    logger = logging.getLogger("rss_reader.database.get_param_for_connect")
    logger.info("get param for connect from config.txt")
    dict_parameters = {}
    with open(filename, "r") as file:
        for line in file:
            key, value = line.split()
            dict_parameters[key] = value
    return dict_parameters


def connect_to_database():
    logger = logging.getLogger("rss_reader.database.connect_to_database")
    logger.info("connect to database")
    if os.path.isfile('final_task/config.txt'):
        filename = "final_task/config.txt"
    elif os.path.isfile('config.txt'):
        filename = 'config.txt'
    else:
        raise psycopg2.OperationalError("check config")

    parameters = get_param_for_connect(filename)
    con = psycopg2.connect(
        database=parameters['database'],
        user=parameters['user'],
        password=parameters['password'],
        host=parameters['host'],
        port=parameters['port']
    )
    return con


def is_table():
    logger = logging.getLogger("rss_reader.database.is_table")
    logger.info("check exist table")
    flag_is_table = True
    with closing(connect_to_database()) as con:
        cursor = con.cursor()

        try:
            cursor.execute("SELECT * FROM NEWS")
        except psycopg2.DatabaseError:
            flag_is_table = False
        finally:
            con.close()
            return flag_is_table


def create_table(con, cursor):
    logger = logging.getLogger("rss_reader.database.create_table")
    logger.info("create table")
    if not is_table():
        cursor.execute('''CREATE TABLE NEWS     
                     (FEED TEXT ,
                     SOURCE_LINK TEXT,
                     TITLE_OF_NEWS TEXT,
                     DATA timestamptz,
                     LINK TEXT ,
                     INFO TEXT,
                     BRIEFLY TEXT,
                     LINKS TEXT[]);''')
        con.commit()


def write_to(list_news: list, source_link: str, cursor):
    logger = logging.getLogger("rss_reader.database.write_to")
    logger.info("write news")
    for news in list_news:
        cursor.execute("SELECT * FROM NEWS WHERE LINK = %s", (news.link,))
        if not cursor.fetchall():
            cursor.execute(
                "INSERT INTO NEWS (FEED,SOURCE_LINK,TITLE_OF_NEWS,DATA,LINK,INFO,BRIEFLY,LINKS) "
                "VALUES (%s,%s, %s,%s, %s, %s, %s,%s)", (news.feed,
                                                         source_link,
                                                         news.title,
                                                         news.date,
                                                         news.link,
                                                         news.info_about_image,
                                                         news.briefly_about_news,
                                                         news.links_from_news,)

            )


def read_news(list_of_news: list, limit: int, source_link, date_of_news: datetime, cursor):
    logger = logging.getLogger("rss_reader.database.read_news")
    logger.info("return cache")
    if limit:
        cursor.execute(
            "SELECT * FROM NEWS WHERE date(DATA) = DATE(%s) AND SOURCE_LINK = %s LIMIT %s",
            (date_of_news, source_link, limit,))
    else:
        cursor.execute("SELECT * FROM NEWS WHERE date(DATA) = DATE(%s) AND SOURCE_LINK = TEXT(%s)",
                       (date_of_news, source_link,))
    if not bool(cursor.rowcount):
        print("Your news story is empty")
    for row in cursor:
        news = News.News(feed=row[0],
                         title=row[2],
                         date=row[3],
                         link=row[4],
                         info_about_image=row[5],
                         briefly_about_news=row[6],
                         links_from_news=row[7])
        list_of_news.append(news)


def clear_the_history(connect, cursor):
    cursor.execute('DELETE  FROM NEWS')
    connect.commit()
