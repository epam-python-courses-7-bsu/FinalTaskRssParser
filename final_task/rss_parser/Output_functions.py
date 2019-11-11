import json
import logging
import re
from itertools import groupby

from bs4 import BeautifulSoup

from final_task.rss_parser.Classes.Novelty import Novelty


def clean_html(raw_html):
    """
    Formatting our String excluding all html-tags making it easier to read our description
    :param raw_html:
    :return:
    """
    logging.info("Cleaning something from htlm-tags.")
    cleaner = re.compile('<.*?>')
    clean_text = re.sub(cleaner, '', raw_html)
    logging.info("Cleaned from html-tags!")
    return clean_text


def printing_corrected(the_feed_entry):
    """
    Output of description in more readable view
    if line is at 116 or further position and our position
     is space - we transfer our string to the next line
     to make our text more readable
    :param the_feed_entry:
    :return:
    """
    logging.info("Changing description to a readable view!")
    position = 0
    string = the_feed_entry
    for char in string:
        print(char, end='')
        position = position + 1
        if position > 106 and (char == ' '):
            print()
            position = 0
    logging.info("Now description is in readable view!")


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
    :param the_feed:
    :param num_of_news:
    :return:
    """
    logging.info("Now getting images from the page.")
    pack_of_img = []
    pack_of_images_links = []
    for num, item in enumerate(the_feed.entries):
        if num == getting_num_of_news(the_feed, num_of_news):
            break
        soup = BeautifulSoup(str(item), "lxml")
        if item.get('media_content', '') != '' and not soup.find_all('img') != []:  # if soup.find_all == []:
                                                                                    # if image link is in media_content: else:
            # go with soup 'img'
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
                        pack_of_images_links.append(num)
    logging.info("Got some images!")
    return pack_of_images_links


def getting_alt_text(the_feed, num_of_news):
    """
    getting alternative text for images
    :param the_feed:
    :param num_of_news:
    :return:
    """
    pack_of_alts = []
    logging.info("Getting alternative text for images!")
    for num, item in enumerate(the_feed.entries):
        if num == getting_num_of_news(the_feed, num_of_news):  # ограничение количества отображаемых новостей
            break
        soup = BeautifulSoup(str(item), "lxml")
        for img in soup.find_all('img'):
            if img is None:
                pack_of_alts.append(num)
            else:
                try:
                    pack_of_alts.append(img['alt'])
                except KeyError:
                    logging.warning("Solving problems with alternative text!")
                    pack_of_alts.append(num)
    logging.info("Got some alternative text.")
    return pack_of_alts


def getting_pack_of_news(the_feed, num_of_news=None):
    """
    Creating full novelty
    1. Adding list of images, correct it if some duplicates are there
    2. Adding list of alternative texts, correct it if some duplicates are there
    3. Some problems can occur if there are no alternative text, solving them with changing list of alts
    :param the_feed:
    :param num_of_news:
    :return:
    """
    if num_of_news > len(the_feed.entries):
        print("You want to get more news than exist.")
        print("Printing all news from the source!")

    print("------------------------")
    print("Source: ", printing_title(the_feed))
    pack_of_news = []
    pack_of_images_links = getting_images_links(the_feed, num_of_news)
    pack_of_alts = getting_alt_text(the_feed, num_of_news)
    # corrected_pack_of_images_links = [el for el, _ in groupby(pack_of_images_links)]
    corrected_pack_of_alts = [el for el, _ in groupby(pack_of_alts)]

    for num, item in enumerate(the_feed.entries):
        if num == num_of_news:  # ограничение количества отображаемых новостей
            break
        pack_of_news.append(getting_novelty(item, num, pack_of_images_links, corrected_pack_of_alts)) # занесение класса Новость в пак новостей
    return pack_of_news


def getting_novelty(item, number, corrected_pack_of_images_links, corrected_pack_of_alts):
    """
    It was really difficult to get images because of variety of templates how sites leave link for image
    Here we create object of Novelty class and fill it with our title, description and etc.
    Then if some problems with images or alt.text occur we use
    :param item:
    :param number:
    :param corrected_pack_of_images_links:
    :param corrected_pack_of_alts:
    :return:
    """

    try:
        novelty = Novelty(number + 1, item.get('title', ''), item.get('published', ''),
                item.get('link', ''), clean_html(item.get('description', '')),
                corrected_pack_of_images_links[number],
                          corrected_pack_of_alts[number])
    except IndexError:
        novelty = Novelty(number + 1, item.get('title', ''), item.get('published', ''),
                          item.get('link', ''), clean_html(item.get('description', '')),
                          corrected_pack_of_images_links[number],
                          corrected_pack_of_alts[0])
    return novelty


def getting_full_info(pack_of_news):
    """
    Getting full info from news
    try-except for printing links and alternative text
    :param pack_of_news:
    :return:
    """
    for novelty in pack_of_news:
        print()
        print("{0}.".format(novelty.number_of_novelty), "Title: ", novelty.title_of_novelty)
        print("Published: ", novelty.time_of_novelty)
        print("Link: ", novelty.source_link)
        print("Description: ")
        printing_corrected(novelty.description)
        try:
            print()
            print("[{0}] {1}".format(1, novelty.source_link))
            if novelty.images_links != novelty.number_of_novelty-1:
                print("[{0}] {1}".format(2, novelty.images_links))
            else:
                print("[{0}] {1}".format(2, "no image"))
            if novelty.alt_text != novelty.number_of_novelty-1:
                print("Alternative text: ", novelty.alt_text)
            else:
                print("Alternative text: ", "no alternative text.")
        except AttributeError:
            print()
            print("[{0}] {1}".format(1, novelty.source_link))
            print("[{0}] {1}".format(2, "No image."))
            print("Alternative text: ", "no alt")


def converting_to_json(the_feed, pack_of_news, num_of_news):
    logging.info("Converting to json view!")
    news_dict = {
        "Source" : the_feed.get('feed', '').get('title'),
        "Number of news" : num_of_news,
        "News":[{"number":item.number_of_novelty,
                 "title":item.title_of_novelty,
                 "published":item.time_of_novelty,
                 "link":item.source_link,
                 "description":item.description,
                 "images links":item.images_links,
                 "alternative text":item.alt_text
                 }for num, item in enumerate(pack_of_news)]
    }
    logging.info("Converted to json view!")
    return json.dumps(news_dict)