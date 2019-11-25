from contextlib import closing
import feedparser
import json
import logging
from database_functions import put_into_db, check_existance, json_from_cashe
from database_functions import open_database
from conversion_functions import convert_into_html_format, convert_into_pdf_format
from information_about_news import InfoAboutNews, taking_information_from_feedparser, printing


def print_cache(dict_of_args):
    """ Prints news from database from the specified day."""

    exists = check_existance("cache")
    if not exists:
        print("There is no cache soon")
        logging.error("Database doesn't exist")
        return None
    with closing(open_database()) as con:
        if con:
            cur = con.cursor()
            if dict_of_args.get("lim") > 0:
                cur.execute("SELECT * from cache WHERE feed = ? AND date = ? LIMIT ?",
                            (dict_of_args.get("url"), dict_of_args.get("date"), str(dict_of_args.get("lim"))))
            else:
                cur.execute("SELECT * from cache WHERE feed = ? AND date = ?",
                            (dict_of_args.get("url"), dict_of_args.get("date")))

            rows = cur.fetchall()
            if not rows:
                print("No results\nTry to enter another date or url")
                logging.debug("No news from this date or url")
                return None
            if dict_of_args.get("json"):
                json_from_cashe(rows)
            elif dict_of_args.get("html"):
                convert_into_html_format(rows, dict_of_args)
            elif dict_of_args.get("pdf"):
                convert_into_pdf_format(rows, dict_of_args)
            else:
                for row in rows:
                    news_info = InfoAboutNews(row)
                    printing(news_info)
        else:
            print("Can't connect to database")
            logging.error("No connection  to database")


def printing_news(feed, dict_of_args):
    """ Prints news"""

    print(feed)
    print("Feed: " + feed.feed.get("title", ""))
    print("__________________________________________________________________")
    for index, feed_entry in enumerate(feed.entries):
        list_of_args = taking_information_from_feedparser(feed_entry, dict_of_args)
        news_info = InfoAboutNews(list_of_args)
        printing(news_info)
        put_into_db(news_info.feed, news_info.title,
                    feed_entry.get("published_parsed", feed.feed.published_parsed),
                    news_info.description, news_info.link, news_info.link_of_img)


def parse_to_json_format(feed, dict_of_args):
    """ Converts to json format and prints"""

    list_to_json = []
    for feed_entry in feed.entries:
        list_of_args = taking_information_from_feedparser(feed_entry, dict_of_args)
        news_info = InfoAboutNews(list_of_args)
        dictionary = {"Title": news_info.title, "Date": news_info.date,
                      "Description": news_info.description, "Link [1]": news_info.link}
        if news_info.link_of_img:
            dictionary.update({"Link [2]": news_info.link_of_img})
        list_to_json.append(dictionary)
        put_into_db(news_info.feed, news_info.title,
                    feed_entry.get("published_parsed", feed.feed.published_parsed),
                    news_info.description, news_info.link, news_info.link_of_img)

    # converts to json
    json_data = json.dumps(list_to_json, indent=5, ensure_ascii=False)
    print(json_data)


def parse(dict_of_args):
    """ Parses news"""

    feed = feedparser.parse(dict_of_args.get("url"))
    if feed.get('bozo') == 1:
        string_exception = feed.get('bozo_exception')
        logging.error(string_exception)
        print(string_exception)
        return None

    logging.debug("Parsing from website was successful")
    if dict_of_args.get("lim") > -1:
        feed.entries = feed.entries[:dict_of_args.get("lim")]
    if dict_of_args.get("json"):
        parse_to_json_format(feed, dict_of_args)
    elif dict_of_args.get("html"):
        convert_into_html_format(feed.entries, dict_of_args)
    elif dict_of_args.get("pdf"):
        convert_into_pdf_format(feed.entries, dict_of_args)
    else:
        printing_news(feed, dict_of_args)
    return None
