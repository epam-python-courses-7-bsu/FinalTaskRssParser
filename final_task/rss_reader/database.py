import sqlite3
import os
import logging as log


database = r"C:\sqlite\db\pythonsqlite.db"


def create_connection(db_file):
    """
        create a database connection to the SQLite database
    """
    connection = None
    try:
        connection = sqlite3.connect(db_file)
        return connection
    except sqlite3.Error as e:
        log.info("Can't connect to database")
        print(e)
    return connection


def create_table(connection, create_table_sql):
    """
        create a table from the create_table_sql statement
    """
    try:
        c = connection.cursor()
        c.execute(create_table_sql)
    except sqlite3.Error as e:
        print(e)


create_projects_table = """ CREATE TABLE IF NOT EXISTS projects (
                                data text PRIMARY KEY,
                                title text NOT NULL,
                                description text,
                                url text); """


def insert_news_into_table():
    pass


# What is cur here?
# def article_is_not_db(article_title, article_date):
#     cur.execute(
#         "SELECT * from myrss WHERE title=? AND date=?",
#         (article_title, article_date)
#     )
#     if not cur.fetchall():
#         return True
#     else:
#         return False
