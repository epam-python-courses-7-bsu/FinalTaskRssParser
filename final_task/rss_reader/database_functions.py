import logging
import sqlite3
import json


def check_existance() -> bool:
    con = open_database()
    flag = False
    try:
        if con:
            cur = con.cursor()
            cur.execute("SELECT * from cache")
            logging.debug("Table exists")
            flag = True
            con.close()
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

    exists = check_existance()
    if not exists:
        create_table()
    con = open_database()
    if con:
        cur = con.cursor()
        if date.tm_hour >= 21:
            date_of_publishing = (str(date.tm_year) + (str(date.tm_mon)) + (str(date.tm_mday + 1)))
        else:
            date_of_publishing = (str(date.tm_year) + (str(date.tm_mon)) + (str(date.tm_mday)))
        cur.execute("INSERT INTO cache VALUES (?, ?, ?, ?, ?, ?)", (url, title, date_of_publishing, text, link, link_of_img))
        con.commit()
    return None

def json_from_cashe(rows):
    """ Convets news from cache in json format"""

    list_to_json_format = []
    for row in rows:
        dictionary = {"Title": row[1],
                      "Date": row[2],
                      "Description": row[3],
                      "Link [1]": row[4]}
        if row[5] != "":
            dictionary.update({"Link [2]": row[5]})
        list_to_json_format.append(dictionary)
    jsonData = json.dumps(list_to_json_format, indent=5, ensure_ascii=False)
    print(jsonData)
    return None

def printing(args):
    """ Just prints news"""

    if args[5] != "":
        print("Title: %s\nDate: %s\nLink: %s\n\n%s\n\nLinks:\n[1]: %s\n[2]: %s" %
              (args[1], args[2], args[4], args[3], args[4], args[5]))
    else:
        print("Title: %s\nDate: %s\nLink: %s\n\n%s\n\nLinks:\n[1]: %s" %
              (args[1], args[2], args[4], args[3], args[4]))
    print("__________________________________________________________________")
