import datetime
import logging
import sqlite3
from contextlib import closing

import News
from exceptions import DataBaseEmpty

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
    con = sqlite3.connect("database.db")  # или :memory: чтобы сохранить в RAM
    return con


def is_table():
    logger = logging.getLogger("rss_reader.database.is_table")
    logger.info("check exist table")
    flag_is_table = True
    with closing(connect_to_database()) as con:
        cursor = con.cursor()

        try:
            cursor.execute("SELECT * FROM NEWS")
        except sqlite3.OperationalError:
            flag_is_table = False

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
                     LINKS TEXT);''')
        con.commit()


def write_to(list_news: list, source_link: str, cursor):
    logger = logging.getLogger("rss_reader.database.write_to")
    logger.info("write news")
    for news in list_news:
        cursor.execute(f"SELECT * FROM NEWS WHERE LINK = ?", (news.link,))
        if not cursor.fetchall():
            links_in_str = ""
            for link in news.links_from_news:
                links_in_str += link + "\n"
            cursor.execute(
                "INSERT INTO NEWS (FEED,SOURCE_LINK,TITLE_OF_NEWS,DATA,LINK,INFO,BRIEFLY,LINKS) "
                "VALUES (?,?, ?,?, ?, ?, ?,?)", (news.feed,
                                                 source_link,
                                                 news.title,
                                                 news.date,
                                                 news.link,
                                                 news.info_about_image,
                                                 news.briefly_about_news,
                                                 links_in_str,)

            )
    logger = logging.getLogger("rss_reader.database.write_to")
    logger.info("end write news")


def read_news(list_of_news: list, limit: int, source_link, date_of_news: datetime, cursor):
    logger = logging.getLogger("rss_reader.database.read_news")
    logger.info("return cache")
    if limit:
        cursor.execute(
            "SELECT * FROM NEWS WHERE date(DATA) = DATE(?) AND SOURCE_LINK = ? LIMIT ?",
            (date_of_news, source_link, limit,))
    else:
        cursor.execute("SELECT * FROM NEWS WHERE date(DATA) = DATE(?) AND SOURCE_LINK = ?",
                       (date_of_news, source_link,))

    for row in cursor:
        links = row[7].split("\n")
        news = News.News(feed=row[0],
                         title=row[2],
                         date=row[3],
                         link=row[4],
                         info_about_image=row[5],
                         briefly_about_news=row[6],
                         links_from_news=links[:-1])
        list_of_news.append(news)
    if not list_of_news:
        raise DataBaseEmpty(Exception("Your news story on is empty "))


def clear_the_history(connect, cursor):
    cursor.execute('DELETE  FROM NEWS')
    connect.commit()
