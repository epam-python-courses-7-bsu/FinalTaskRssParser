from contextlib import closing
import logging
import pymysql
from personal_exceptions import DatabaseConnectionError


def get_news_list_by_date(date, limit):
    """
    :param date: Date of publication of news
    :return: : List with news publicated by date
    Returns list of news by date from database
    """
    logging.info('Connecting to database')
    try:
        with closing(pymysql.connect(host='localhost', user='root', password='Password12345',
                                     database='final_task_database')) as connection:
            with closing(connection.cursor()) as cursor:
                logging.info('Connected to database')
                logging.info('Giving request')
                try:
                    cursor.execute(f'select * from news_cache where date="{date}"')
                except pymysql.err.InternalError:
                    logging.error('Input value of --date is incorrect')
                    raise ValueError('Input value of --date is incorrect')
                logging.info('Getting response')
                database_response = cursor.fetchall()
                if limit:
                    limit = min(len(database_response), limit)
                else:
                    limit = len(database_response)
                logging.info('Response was got')
                news_list = []
                for index in range(limit):
                    news_list.append({'Feed': database_response[index][0],
                                      'Title': database_response[index][1],
                                      'Date': database_response[index][2],
                                      'Link': database_response[index][3],
                                      'Image description': database_response[index][4],
                                      'New description': database_response[index][5],
                                      'Image links': database_response[index][6].split('|||')})
                return news_list
    except pymysql.err.OperationalError:
        logging.error('Not connected to database')
        raise DatabaseConnectionError("Can't connect to database, check if you have installed Mysql, and necessary"
                                      "database with table described in README")


def write_news_to_database(news_list):
    """
    :param news_list: List of news
    Writes news to database
    """
    logging.info('Connecting to database')
    try:
        with closing(pymysql.connect(host='localhost', user='root', password='Password12345',
                                     database='final_task_database')) as connection:
            with closing(connection.cursor()) as cursor:
                logging.info('Connected to database')
                for new in news_list:
                    # Try to find new in database by link, if exists
                    cursor.execute(f'select * from news_cache where link = "{new["Link"]}"')
                    if cursor.fetchall():
                        continue
                    insert_values = [value for value in new.values()]
                    insert_values[6] = '|||'.join(insert_values[6])
                    insert_values = [tuple(insert_values), ]
                    cursor.executemany('Insert into news_cache values(%s,%s,%s,%s,%s,%s,%s)', insert_values)
                connection.commit()
        logging.info('Data write successful')
    except pymysql.err.OperationalError:
        logging.error('Not connected to database')
        raise DatabaseConnectionError("Can't connect to database, check if you have installed Mysql, and necessary"
                                      "database with table described in README")
