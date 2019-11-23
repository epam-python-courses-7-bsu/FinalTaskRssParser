import sys
import feedparser
import json
import logging
import requests
from yattag import Doc
from fpdf import FPDF
import os
from database_functions import put_into_db, check_existance, json_from_cashe
from database_functions import open_database, printing

class RssParser():
    """ Parses news from website"""
    def __init__(self, *args):
        """ Inits arguments"""

        self.url = args[0]
        self.limit = args[1]
        self.jsonFormat = args[2]
        self.date = args[3]
        self.to_html = args[5]
        self.path = args[4]
        self.to_pdf = args[6]
        logging.debug("Check in parser")
        if self.date:
            self.print_cashe()
        else:
            self.parse()

    def print_cashe(self):
        """ Prints news from database from the specified day."""
        exists = check_existance()
        if not exists:
            print("There is no cache soon")
            return None
        con = open_database()

        if con:
            cur = con.cursor()
            if self.limit > 0:
                cur.execute("SELECT * from cache WHERE feed = ? AND date = ? LIMIT ?",
                            (self.url, self.date, str(self.limit)))
            else:
                cur.execute("SELECT * from cache WHERE feed = ? AND date = ?", (self.url, self.date))

            rows = cur.fetchall()
            if not rows:
                print("No results\nTry to enter another date or url")
                return None
            if self.jsonFormat:
                json_from_cashe(rows)
            elif self.to_html:
                self.convert_into_html_format(rows)
            elif self.to_pdf:
                self.convert_into_pdf_format(rows)
            else:
                for row in rows:
                    printing(row)
            con.close()
        else:
            print("Can't connect to database")

    def convert_into_html_format(self, thefeed):
        """ Creates html file in specified directory and puts information in database, if it was read from website"""

        # openning html-file to write
        if not os.path.exists(self.path):
            print("Invalid directory")
            return None
        filename = os.path.join(self.path, "news.html")
        file = open(filename, 'w')
        logging.debug("File was opened successfully")

        doc, tag, text, line = Doc().ttl()
        line('h1', 'News from ' + self.url)

        for thefeedentry in thefeed:
            # getting list of tags
            if self.date == None:
                list_of_tags = self.taking_information_from_feedparser(thefeedentry)
            else:
                list_of_tags = thefeedentry
            link_of_img = ""
            with tag('item'):
                with tag('h2'):
                    text(list_of_tags[1])
                with tag('link'):
                    text(list_of_tags[4])
                with tag('p'):
                    text(list_of_tags[2])
                with tag('h3'):
                    if list_of_tags[5]:
                        with tag('img', src=list_of_tags[5], alt=list_of_tags[5], border="0", align="left", hspace="5"):
                            pass
                    text(list_of_tags[3])
                with tag('br'):
                    with tag('br'):
                        pass

            # putting news in database
            if self.date == None:
                put_into_db(list_of_tags[0], list_of_tags[1],
                          thefeedentry.get("published_parsed", thefeedentry.published_parsed),
                          list_of_tags[3], list_of_tags[4], list_of_tags[5])
        try:
            file.write(doc.getvalue())
            print("News were written in html file")
        except Exception:
            logging.error(Exception)
            print("Can't write information in html file")
        finally:
            file.close()

    def convert_into_pdf_format(self, thefeed):
        """ Creates pdf file in specified directory and puts information in database, if it was read from website"""

        if not os.path.exists(self.path):
            print("Invalid directory")
            return None
        filename = os.path.join(self.path, "news.pdf")
        logging.debug("File was opened successfully")

        if sys.platform == 'win32':
            font_path = r'C:\Windows\Fonts\arial.ttf'
            if not os.path.isfile(font_path):
                font_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'ARIALUNI.TTF')
        if sys.platform == 'linux':
            font_path = r'/usr/share/fonts/dejavu/DejaVuSansCondensed.ttf'
            if not os.path.isfile(font_path):
                font_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'ARIALUNI.TTF')

        pdf = FPDF()
        pdf.add_page(('P', 'A4'))
        pdf.add_font('arial_uni', '', font_path, True)
        pdf.set_margins(10, 10, 10)
        count = 0

        for thefeedentry in thefeed:
            if self.date == None:
                list_of_tags = self.taking_information_from_feedparser(thefeedentry)
            else:
                list_of_tags = thefeedentry

            pdf.set_font("arial_uni", size=14)
            pdf.multi_cell(200, 10, txt=(list_of_tags[1] + "\n"), align="C")
            pdf.set_font("arial_uni", size=10)
            pdf.multi_cell(200, 8, txt=list_of_tags[2], align="C")
            pdf.set_font("arial_uni", size=8)
            pdf.multi_cell(0, 8, txt=list_of_tags[4], align="C")

            if list_of_tags[5]:
                try:
                    img = requests.get(list_of_tags[5])
                    out = open("img" + str(count) + ".jpg", "wb")
                    out.write(img.content)
                    out.close()
                    pdf.image("img" + str(count) + ".jpg", x=100, w=20)
                    count += 1
                except requests.exceptions.ConnectionError:
                    print("Can't download image, because of connection to the Internet")
                    pdf.multi_cell(0, 8, txt=list_of_tags[5], align="C")
                    logging.error(requests.exceptions.ConnectionError)
            pdf.set_font("arial_uni", size=10)
            pdf.multi_cell(0, 6, txt=list_of_tags[3], align="C")
            pdf.multi_cell(200, 10, txt="_________________\n", align="C")

            # putting news in database
            if self.date == None:
                put_into_db(list_of_tags[0], list_of_tags[1],
                          thefeedentry.get("published_parsed", thefeedentry.published_parsed),
                          list_of_tags[3], list_of_tags[4], list_of_tags[5])
        try:
            pdf.output(filename)
            print("News were written in pdf file")

            for i in range(count):
                os.remove("img" + str(i) + ".jpg")
        except Exception:
            logging.error(Exception)
            print("Can't write information in pdf file")

    def find_description(self, description) -> str:
        """ Parses description in readable format, return description"""

        text = description
        index_of_text_beginning = description.find(">")
        while index_of_text_beginning != -1:
            if index_of_text_beginning != len(description) - 1:
                if description[index_of_text_beginning + 1] != "<":
                    text = description[index_of_text_beginning + 1:]
                    text = text[: text.find('<')]
                    break
            description = description[index_of_text_beginning + 1:]
            index_of_text_beginning = description.find(">")
        return text

    def printing_news(self, thefeed):
        """ Prints news"""

        print("Feed: " + thefeed.feed.get("title", ""))
        print("__________________________________________________________________")
        for index, thefeedentry in enumerate(thefeed.entries):
            list_of_tags = self.taking_information_from_feedparser(thefeedentry)
            printing(list_of_tags)
            put_into_db(list_of_tags[0], list_of_tags[1],
                        thefeedentry.get("published_parsed", thefeed.feed.published_parsed),
                        list_of_tags[3], list_of_tags[4], list_of_tags[5])

    def taking_information_from_feedparser(self, thefeedentry) -> list:
        """ Creates a list with arguments: title, date, link, description, link of image and description of image, if
        they exist for each news"""

        list_of_args = [self.url, thefeedentry.get("title", ""), thefeedentry.get("published", "")]
        description = thefeedentry.get("description", "")
        description_to_put = self.find_description(description)

        # trying to get link of image and description of image
        index_of_link = description.find("src")
        link_of_img = ""
        if index_of_link != -1:
            link_of_img = description[index_of_link + 5:]
            link_of_img = link_of_img[: link_of_img.find('"')]

            index_of_link = description.find("alt")
            alt_of_img = description[index_of_link + 5:]
            alt_of_img = alt_of_img[: alt_of_img.find('"')]

            description_to_put = "[image: " + alt_of_img + "][2]" + description_to_put
        list_of_args.append(description_to_put)
        list_of_args.append(thefeedentry.get("link", ""))
        list_of_args.append(link_of_img)
        return list_of_args

    def parse_to_json_format(self, thefeed):
        """ Converts to json format and prints"""

        list_to_json = []
        for index, thefeedentry in enumerate(thefeed.entries):
            list_of_tags = self.taking_information_from_feedparser(thefeedentry)
            dictionary = {"Feed": thefeed.feed.get("title", ""), "Title": list_of_tags[0],
                          "Date": list_of_tags[1], "Description": list_of_tags[3], "Link [1]": list_of_tags[4]}
            if list_of_tags[5] != "":
                dictionary.update({"Link [2]": list_of_tags[5]})
            list_of_tags.append(dictionary)
            put_into_db(list_of_tags[0], list_of_tags[1],
                        thefeedentry.get("published_parsed", thefeed.feed.published_parsed),
                        list_of_tags[3], list_of_tags[4], list_of_tags[5])

        # converts to json
        json_data = json.dumps(list_to_json, indent=5, ensure_ascii=False)
        print(json_data)

    def parse(self):
        """ Parses news"""

        thefeed = feedparser.parse(self.url)
        if thefeed.get('bozo') == 1:
            string_exception = thefeed.get('bozo_exception')
            logging.error(string_exception)
            print(string_exception)
            return None

        logging.debug("Parsing from website was successful")
        if self.limit > -1:
            thefeed.entries = thefeed.entries[:self.limit]
        if self.jsonFormat:
            self.parse_to_json_format(thefeed)
        elif self.to_html:
            self.convert_into_html_format(thefeed.entries)
        elif self.to_pdf:
            self.convert_into_pdf_format(thefeed.entries)
        else:
            self.printing_news(thefeed)
        return None
