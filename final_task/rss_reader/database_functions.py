import logging
import psycopg2

def readingPasswordFromFile() -> str:
    try:
        f = open('password.txt')
        password = f.readline()
        f.close()
    except "FileNotFoundError":
        logging.error("Can't open file")
        print("Can't open file with password")
        password = "1234"
    return password

def checkExistance() -> bool:
    con = None
    flag = True
    try:
        con = psycopg2.connect(
            database="postgres",
            user="postgres",
            password=readingPasswordFromFile(),
            host="localhost",
            port="5432"
        )

        cur = con.cursor()
        cur.execute("SELECT * from cache")
        logging.debug("Table exists")
    except (Exception, psycopg2.DatabaseError) as error:
        flag = False
        logging.debug("Table doesn't exist")
        logging.error(error)
    finally:
        if con is not None:
            con.close()
        return flag


def createTable():
    con = None
    try:
        con = psycopg2.connect(
            database="postgres",
            user="postgres",
            password=readingPasswordFromFile(),
            host="localhost",
            port="5432"
        )
        cur = con.cursor()
        cur.execute(
            "CREATE TABLE cache(feed TEXT, title TEXT, date TEXT, description TEXT, links TEXT[], PRIMARY KEY (title, date))")
        con.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        logging.error(error)
    finally:
        if con is not None:
            con.close()

def putIntoDB(url, title, date, text, link, linkOfImg):
    """ Writes infomation about news in database"""

    con = None
    exists = checkExistance()
    if not exists:
        createTable()
    try:
        con = psycopg2.connect(
            database="postgres",
            user="postgres",
            password=readingPasswordFromFile(),
            host="localhost",
            port="5432"
        )
        logging.debug("Database opened successfully")
        cur = con.cursor()

        if date.tm_hour >= 21:
            dateOfPublishing = (str(date.tm_year) + (str(date.tm_mon)) + (str(date.tm_mday + 1)))
        else:
            dateOfPublishing = (str(date.tm_year) + (str(date.tm_mon)) + (str(date.tm_mday)))
        if (linkOfImg != ""):
            cur.execute("INSERT INTO cache VALUES (%s, %s, %s, %s, %s)",
                        (url, title, dateOfPublishing, text, '{' + link + ', ' + linkOfImg + '}'))
        else:
            cur.execute("INSERT INTO cache VALUES (%s, %s, %s, %s, %s)",
                        (url, title, dateOfPublishing, text, '{' + link + ',' + '}'))
        con.commit()
    except (Exception, psycopg2.errors.UniqueViolation) as error:
        logging.error("In data base already exists such a row")
    except (Exception, psycopg2.DatabaseError) as error:
        logging.error(error)
    finally:
        if con is not None:
            con.close()
    return None