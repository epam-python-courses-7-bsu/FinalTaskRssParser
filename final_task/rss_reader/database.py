import datetime
import logging
import sqlite3

import News
from exceptions import DataBaseEmpty

MODULE_LOGGER = logging.getLogger("rss_reader.database")


def connect_to_database(name_database: str):
    logger = logging.getLogger("rss_reader.database.connect_to_database")
    logger.info("connecting to database")
    con = sqlite3.connect(f"{name_database}")
    logger.info("connected to database")
    return con


def is_table(connect, table_name: str, name_database: str) -> bool:
    """
    Checks table existence
    :param connect:
    :param name_database:
    :param table_name:
    :return: True or False
    """
    logger = logging.getLogger("rss_reader.database.is_table")
    logger.info("check exist table")
    flag_is_table = True

    cursor = connect.cursor()

    try:
        cursor.execute(f"SELECT * FROM {table_name}")
        logger.info(" table exist")
    except sqlite3.OperationalError:
        flag_is_table = False
        logger.error("table does not exist")

    return flag_is_table


def create_table(con, cursor, name_database_str):
    """
    Creates a table NEWS
    """
    logger = logging.getLogger("rss_reader.database.create_table")
    logger.info("creating table")
    if not is_table(con, "NEWS", name_database_str):
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
    logger.info("created table")


def write_to(list_news: list, source_link: str, cursor):
    """
    Writes news to database
    :param list_news:
    :param source_link:
    :param cursor:
    :return:
    """
    try:
        logger = logging.getLogger("rss_reader.database.write_to")
        logger.info("write news")
        for news in list_news:
            cursor.execute(f"SELECT * FROM NEWS WHERE LINK = ?", (news.link,))
            if not cursor.fetchall():
                # links_in_str = ""
                # for link in news.links_from_news:
                links_in_str = "\n".join(news.links_from_news)
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
        logger.info("end news recording")
    except MemoryError:
        logger = logging.getLogger("rss_reader.database.write_to")
        logger.error("not enough memory")
        raise MemoryError("You do not have enough memory to cache")


def read_news(list_of_news: list, limit: int, source_link, date_of_news: datetime, cursor):
    """
    Read news from database
    :param list_of_news:
    :param limit:
    :param source_link:
    :param date_of_news:
    :param cursor:
    :return:
    """
    logger = logging.getLogger("rss_reader.database.read_news")
    #  the user enter "source_link"
    if limit and source_link:
        logger.info("reading new from cache with limit")
        cursor.execute(
            "SELECT * FROM NEWS WHERE date(DATA) = DATE(?) AND SOURCE_LINK = ? LIMIT ?",
            (date_of_news, source_link, limit,))
    elif not limit and source_link:
        logger.info("reading new from cache without limit")
        cursor.execute("SELECT * FROM NEWS WHERE date(DATA) = DATE(?) AND SOURCE_LINK = ?",
                       (date_of_news, source_link,))
    # the user did not enter "source_link"
    if limit and not source_link:
        logger.info("reading all news from cache with limit ")
        cursor.execute(
            "SELECT * FROM NEWS WHERE date(DATA) = DATE(?) LIMIT ?",
            (date_of_news, limit,))
    elif not limit and not source_link:
        logger.info("reading all news from cache without limit")
        cursor.execute("SELECT * FROM NEWS WHERE date(DATA) = DATE(?)",
                       (date_of_news,))

    for row in cursor:
        links = row[7].split("\n")
        news = News.News(feed=row[0],
                         title=row[2],
                         date=row[3],
                         link=row[4],
                         info_about_image=row[5],
                         briefly_about_news=row[6],
                         links_from_news=links)
        list_of_news.append(news)
    if not list_of_news:
        logger.error("story on is empty")
        raise DataBaseEmpty(Exception("Your news story on is empty "))
    logger.error("news read successfully")


def clear_the_history(connect, name_database, name_table):
    logger = logging.getLogger("rss_reader.database.clear_the_history")
    if is_table(connect, name_table, name_database):
        cursor = connect.cursor()
        cursor.execute(f'DELETE  FROM {name_table}')
        connect.commit()
    print('The story is cleared')
    logger.info('The story is cleared')
