import logging
import sqlite3
import json
from contextlib import closing
from information_about_news import InfoAboutNews


def check_existance(name) -> bool:
    with closing(open_database()) as con:
        flag = False
        try:
            if con:
                cur = con.cursor()
                cur.execute("SELECT * from " + name)
                logging.debug("Table exists")
                flag = True
        except Exception:
            flag = False
        return flag


def create_table():
    con = open_database()
    if con:
        cur = con.cursor()
        cur.execute("CREATE TABLE cache(feed TEXT, title TEXT, date TEXT, description TEXT, link1 TEXT, link2 TEXT,"
                    "UNIQUE (title, date) ON CONFLICT IGNORE)")
        con.commit()
    con.close()


def open_database():
    con = None
    try:
        con = sqlite3.connect("mydatabase.db")
        logging.debug("Database opened successfully")
        cur = con.cursor()
        return con
    except (sqlite3.DatabaseError) as error:
        logging.error(error)
        return None


def put_into_db(url, title, date, text, link, link_of_img):
    """ Writes infomation about news in database"""

    exists = check_existance("cache")
    if not exists:
        create_table()
    with closing(open_database()) as con:
        if con:
            cur = con.cursor()
            date_of_publishing = (str(date.tm_year) + (str(date.tm_mon)) + (str(date.tm_mday)))
            cur.execute("INSERT INTO cache VALUES (?, ?, ?, ?, ?, ?)", (url, title, date_of_publishing, text, link,
                                                                        link_of_img))
            con.commit()


def json_from_cashe(rows):
    """ Convets news from cache in json format"""

    list_to_json_format = []
    for row in rows:
        news_info = InfoAboutNews(row)
        dictionary = {"Title": news_info.title,
                      "Date": news_info.date,
                      "Description": news_info.description,
                      "Link [1]": news_info.link}
        if news_info.link_of_img:
            dictionary.update({"Link [2]": news_info.link_of_img})
        list_to_json_format.append(dictionary)
    json_data = json.dumps(list_to_json_format, indent=5, ensure_ascii=False)
    print(json_data)
