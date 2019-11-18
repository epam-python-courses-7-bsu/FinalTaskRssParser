import json
import logging
import re
import pprint
import sqlite3
from datetime import datetime
from itertools import groupby
from html import unescape

from bs4 import BeautifulSoup

from Classes.Novelty import Novelty


def clean_html(raw_html):
    """
    Formatting our String excluding all html-tags making it easier to read our description
    """
    logging.info("Cleaning something from htlm-tags.")
    cleaner = re.compile('<.*?>')
    clean_text = re.sub(cleaner, '', raw_html)
    logging.info("Cleaned from html-tags!")
    return clean_text


def printing_title(the_feed) -> str:
    logging.info("Getting title.")
    source_title = the_feed.get('feed', '').get('title')
    logging.info("Got title.")
    return source_title


def getting_num_of_news(the_feed, num_of_news):
    if num_of_news is None:
        return len(the_feed.entries)
    else:
        return num_of_news


def getting_images_links(the_feed, num_of_news) -> list:
    """
    due to variety of web sites templates how to carry link for an image I needed variety of solutions
    to get links
    1. Step into entries of feed
    2. Use soup for each item of entries
    3. Compare item with different forms of where links can be
    """
    logging.info("Now getting images from the page.")
    pack_of_img = []
    pack_of_images_links = []
    for num, item in enumerate(the_feed.entries[:num_of_news]):
        soup = BeautifulSoup(str(item), "lxml")
        if item.get('media_content', '') != '' and not soup.find_all('img') != []:  # if soup.find_all == []:
            for image in range(getting_num_of_news(the_feed, num_of_news)):
                pack_of_images_links.append(item.get('media_content', '')[0].get('url', ''))
        else:
            try:
                pack_of_img.append(soup.find('img'))
                if soup.find('img') is not None:
                    pack_of_images_links.append(pack_of_img[num]['src'])
                else:
                    pack_of_images_links.append('No image')
            except IndexError:
                logging.warning("Some problems appeared, solving them!")
                for img in soup.find_all('img'):
                    if img.get('src') != '':
                        pack_of_images_links.append(img.get('src'))
                    else:
                        pack_of_images_links.append(str(num))
    logging.info("Got some images!")
    return pack_of_images_links


def getting_alt_text(the_feed, num_of_news):
    """
    getting alternative text for images:
    """
    pack_of_alts = []
    logging.info("Getting alternative text for images!")
    try:
        for num, item in enumerate(the_feed.entries[:num_of_news]):
            soup = BeautifulSoup(str(item), "lxml")
            for img in soup.find_all('img'):
                if img is None:
                    pack_of_alts.append(str(num))
                else:
                    try:
                        pack_of_alts.append(img['alt'])
                    except KeyError:
                        logging.warning("Solving problems with alternative text!")
                        pack_of_alts.append(str(num))
    except IndexError:
        pass
    logging.info("Got some alternative text.")
    return pack_of_alts


def getting_pack_of_news(the_feed, main_source, num_of_news=None):
    """
    Creating full novelty
    1. Adding list of images, correct it if some duplicates are there
    2. Adding list of alternative texts, correct it if some duplicates are there
    3. Some problems can occur if there are no alternative text, solving them with changing list of alts
    """
    if getting_num_of_news(the_feed, num_of_news) > len(the_feed.entries):
        print("You want to get more news than we can get!")
        print("Printing all news from the storage!")

    pack_of_news = []
    pack_of_news_for_db = []
    pack_of_images_links = getting_images_links(the_feed, num_of_news)
    pack_of_alts = getting_alt_text(the_feed, num_of_news)
    corrected_pack_of_alts = [el for el, _ in groupby(pack_of_alts)]

    for num, item in enumerate(the_feed.entries[:num_of_news]):
        novelty, novelty_for_database = getting_novelty(item, num, pack_of_images_links, corrected_pack_of_alts,
                                                        main_source)
        pack_of_news.append(novelty)
        pack_of_news_for_db.append(novelty_for_database)
    return pack_of_news, pack_of_news_for_db


def getting_novelty(item, number, corrected_pack_of_images_links, corrected_pack_of_alts, main_source):
    """
    It was really difficult to get images because of variety of templates how sites leave link for image
    Here we create object of Novelty class and fill it with our title, description and etc.
    Then if some problems with images or alt.text occur we use
    """

    try:
        alt_text = corrected_pack_of_alts[number]
    except IndexError:
        alt_text = 'No alternative text.'
    novelty = Novelty(number + 1, unescape(item.get('title', '')),
                      item.get('published', ''),
                      item.get('link', ''),
                      unescape(clean_html(item.get('description', ''))),
                      corrected_pack_of_images_links[number],
                      unescape(alt_text),
                      getting_corrected_time(item),
                      main_source)
    novelty_for_database = (novelty.number_of_novelty, novelty.title_of_novelty, novelty.time_of_novelty,
                            novelty.source_link, novelty.description, novelty.images_links,
                            novelty.alt_text, novelty.date_corrected, novelty.main_source)
    return novelty, novelty_for_database


def getting_full_info(the_feed, pack_of_news):
    """
    Getting full info from news
    try-except for printing links and alternative text
    """
    print("------------------------")
    print("Source: ", printing_title(the_feed))
    for novelty in pack_of_news:
        print()
        print("{0}.".format(novelty.number_of_novelty), "Title: ", novelty.title_of_novelty)
        print("Published: ", novelty.time_of_novelty)
        print("Link: ", novelty.source_link)
        print("Description: ")
        print(pprint.pformat(novelty.description, width=115))
        try:
            print()
            print("[{0}] {1}".format(1, novelty.source_link))
            if novelty.images_links != novelty.number_of_novelty - 1:
                print("[{0}] {1}".format(2, novelty.images_links))
            else:
                print("[{0}] {1}".format(2, "no image"))
            if novelty.alt_text != str(novelty.number_of_novelty - 1):
                print("Alternative text: ", novelty.alt_text)
            else:
                print("Alternative text: ", "no alternative text.")
        except AttributeError:
            print()
            print("[{0}] {1}".format(1, novelty.source_link))
            print("[{0}] {1}".format(2, "No image."))
            print("Alternative text: ", "no alt")


def converting_to_json(pack_of_news, the_feed=''):
    logging.info("Converting to json view!")
    try:
        source = the_feed.get('feed', '').get('title')
    except AttributeError:
        source = ''
    news_dict = {
            "Source": source,
            "Number of news": len(pack_of_news),
            "News": [{"number": item.number_of_novelty,
                      "title": item.title_of_novelty,
                      "published": item.time_of_novelty,
                      "link": item.source_link,
                      "description": item.description,
                      "images links": item.images_links,
                      "alternative text": item.alt_text,
                      "corrected time": item.date_corrected,
                      "main source": item.main_source,
                      } for num, item in enumerate(pack_of_news)]
        }
    logging.info("Converted to json view!")
    return json.dumps(news_dict)


def getting_info_into_file(item):
    """
    Preparing information to be written into the file in more readable way
    :param item:
    :return:
    """
    novelty = "\n{0}.\nTitle: {1}\nDate: {2}\nLink: {3}\nDescription:\n {4}\nImages links:{5}\nAlternative text:{6}\n" \
              "Main source: {7}" \
        .format(item.number_of_novelty,
                pprint.pformat(item.title_of_novelty, width=115),
                item.time_of_novelty,
                pprint.pformat(item.source_link, width=115),
                pprint.pformat(item.description.replace("\xa0", " "), width=115),
                pprint.pformat(item.images_links),
                pprint.pformat(item.alt_text, width=115),
                item.main_source)
    return novelty


def getting_corrected_time(item):
    """
    Getting time in view %Y%m%d
    """
    corrected_date = datetime.strptime(item.get('published', ''), '%a, %d %b %Y %X %z')
    return corrected_date.strftime('%Y%m%d')


def getting_time_for_json(item):
    corrected_date = datetime.strptime(item, '%a, %d %b %Y %X %z')
    return corrected_date.strftime('%Y%m%d')


def reading_file(name_of_file):
    with open(name_of_file, 'r', encoding='utf-8') as news_cache:
        return news_cache.read()


def writing_to_file(pack_of_news, pack_of_news_for_db, filename):
    """
    Writing information into 2 files: News_cache.txt and News_cache_json.json
    Creating 2 files because it's easier to read information into computer from JSON file than another file
    1. Open file
    2. Check if file is empty or not
    3. If empty - append whole information
       If Not empty:
              1. Check if the novelty in file
              2. If in file: continue
                 If Not in the file: Find out length of file (amount of news), put that number to incoming novelty
    If that novelty exists it will go to another novelty in limit
    It means that if you enter --limit 15 and 10 news are already in list it will add only 5 news to list
    """
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute('create table if not exists projects(num integer, title text, time text, source_link text, '
                   'description text, images_links text, alt_tx text, date_corrected integer, main_source text)')
    conn.commit()
    logging.info("Opening file News_cache.")
    with open(filename, 'a', encoding='utf-8') as news_cache:
        logging.info("Reading from News_cache.")
        content = reading_file('News_cache.txt')
        if not content:
            if cursor.execute("SELECT * FROM projects"):
                cursor.execute("DELETE FROM projects")
                conn.commit()
            for num, item in enumerate(pack_of_news):
                logging.info("Writing into file if it was empty.")
                news_cache.write(getting_info_into_file(item))
                news_cache.write("\n_ _ _")
                cursor.execute('insert into projects values (?,?,?,?,?,?,?,?,?)', pack_of_news_for_db[num])
                conn.commit()
        else:
            for number, item in enumerate(pack_of_news):
                if item.source_link in content:
                    continue
                else:
                    length = sum(1 for line in cursor.execute("SELECT * FROM projects")) + 1
                    logging.info("Counting lines.")
                    logging.info("Counted lines.")
                    item.number_of_novelty = length
                    logging.info("Writing into file if it was not empty.")
                    news_cache.write(getting_info_into_file(item))
                    news_cache.write("\n_ _ _")
                    cursor.execute('insert into projects values (?,?,?,?,?,?,?,?,?)', pack_of_news_for_db[number])
                    conn.commit()
    conn.close()


def getting_from_database_to_pack():
    pack_of_news = []
    with sqlite3.connect("database.db") as conn:
        cursor = conn.cursor()
        for item in cursor.execute("SELECT * FROM projects"):
            (number, title, date, source, description, im_links, alt, date_corr, main_source) = item
            novelty = Novelty(number, title, date, source, description, im_links, alt, date_corr, main_source)
            pack_of_news.append(novelty)
    return pack_of_news


def verbose(list_of_args):
    if '--verbose' in list_of_args:
        print()
        with open('Snake.log') as log:
            for line in log:
                print(line)
