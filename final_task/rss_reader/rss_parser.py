import feedparser
import json
import logging
import psycopg2
from yattag import Doc
from database_functions import checkExistance
from database_functions import createTable
from database_functions import putIntoDB
from database_functions import readingPasswordFromFile

class RssParser():
    """ Parses news from website"""

    url = ""
    limit = 0
    date = None
    jsonFormat = False
    path = None
    to_html = False

    def __init__(self, parametrUrl, parametrLimit, parametrJsonFormat = False, parametrDate = None, parametrPath = None,
                 parametrHtml = False):
        """ Inits arguments"""

        self.url = parametrUrl
        self.limit = parametrLimit
        self.jsonFormat = parametrJsonFormat
        self.date = parametrDate
        self.to_html = parametrHtml
        self.path = parametrPath
        logging.debug("Check in parser")

        if self.date != None:
            self.printCashe()
        else:
            self.parse()

    def jsonFromCashe(self, rows):
        """ Convets news from cache in json format"""

        listToJsonFormat = []
        for row in rows:
            if len(row[4]) > 1:
                dictionary = {"Title": row[1],
                              "Date": row[2],
                              "Description": row[3],
                              "Link [1]": row[4][0],
                              "Link [2]": row[4][1]}
            else:
                dictionary = {"Title": row[1],
                              "Date": row[2],
                              "Description": row[3],
                              "Link [1]": row[4][0]}
            listToJsonFormat.append(dictionary)
        jsonData = json.dumps(listToJsonFormat, indent=5, ensure_ascii=False)
        print(jsonData)
        return None

    def htmlFromCashe(self, rows):
        """ Converts news from cache in html format"""

        filename = self.path + r"\news.html"
        try:
            f = open(filename, 'w')
        except OSError:
            logging.error("File can't be opened")
            print("Could not open file ", filename)
            return None
        logging.debug("File was opened successfully")
        doc, tag, text, line = Doc().ttl()
        line('h1', 'News from ' + self.url)
        for row in rows:
            with tag('item'):
                with tag('h2'):
                    text(row[1])
                with tag('link'):
                    text(row[4][0])
                with tag('h3'):
                    if len(row[4]) > 1:
                        with tag('img', src=row[4][1], border="0", align="left", hspace="5"):
                            pass
                    text(row[3])
                with tag('br'):
                    pass
        try:
            f.write(doc.getvalue())
            print("News were written in html file")
            logging.debug("News were written in html file")
        except Exception:
            logging.error(Exception)
        finally:
            f.close()
        return None

    def printCashe(self):
        """ Prints news from database from the specified day."""

        logging.debug("Check in printCashe")
        con = None
        exists = checkExistance()
        if not exists:
            createTable()
        try:
            con = psycopg2.connect(
                database="postgres",
                user="postgres",
                password=readingPasswordFromFile(),
                host="127.0.0.1",
                port="5432"
            )
            logging.debug("Database opened successfully")
            cur = con.cursor()
            if self.limit > 0:
                cur.execute("SELECT * from cache WHERE feed = %s AND date = %s LIMIT %s",
                            (self.url, self.date, str(self.limit)))
            else:
                cur.execute("SELECT * from cache WHERE feed = %s AND date = %s", (self.url, self.date))

            rows = cur.fetchall()
            if not rows:
                print("No results\nTry to enter another date or url")
                return None
            if self.jsonFormat:
                self.jsonFromCashe(rows)
            elif self.to_html:
                self.htmlFromCashe(rows)
            else:
                for row in rows:
                    print("Title: ", row[1])
                    print("Date: ", row[2])
                    print("Link: ", row[4][0])
                    print()
                    print("Description: " + row[3])
                    print("\nLinks:")
                    print("[1]:", row[4][0])
                    if len(row[4]) > 1:
                        print("[2]:", row[4][1])
                    print("__________________________________________________________________")
        except (psycopg2.DatabaseError) as error:
            logging.error(error)
        except Exception as error:
            logging.error(error)
        finally:
            if con is not None:
                con.close()
        return None

    def convertIntoHtmlFormat(self, thefeed):
        """ Creates html file in specified directory and puts information in database"""

        # openning html-file to write
        filename = self.path + r"\news.html"
        try:
            f = open(filename, 'w')
        except OSError:
            logging.error("File can't be opened")
            print("Could not open file ", filename)
            return None
        logging.debug("File was opened successfully")

        doc, tag, text, line = Doc().ttl()
        line('h1', 'News from ' + thefeed.feed.get("title", ""))

        for index, thefeedentry in enumerate(thefeed.entries):
            if (index < self.limit) | (self.limit == -1):
                # getting list of tags
                listOfTags = self.takingInformationFromFeedparser(thefeedentry)
                linkOfImg = ""
                with tag('item'):
                    with tag('h2'):
                        text(listOfTags[0])
                    with tag('link'):
                        text(listOfTags[2])
                    with tag('p'):
                        text(listOfTags[1])
                    with tag('h3'):
                        if len(listOfTags) > 4:
                            linkOfImg = listOfTags[4]
                            with tag('img', src=linkOfImg, alt=listOfTags[5], border="0", align="left", hspace="5"):
                                pass
                        text(listOfTags[3])
                    with tag('br'):
                        pass
                    with tag('br'):
                        pass

                # putting news in database
                putIntoDB(listOfTags[2], listOfTags[0],
                          thefeedentry.get("published_parsed", thefeed.feed.published_parsed),
                          listOfTags[3], listOfTags[2], linkOfImg)
        try:
            f.write(doc.getvalue())
            print("News were written in html file")
            logging.debug("News were written in html file")
        except Exception:
            logging.error(Exception)
            print("Can't write information in html file")
        finally:
            f.close()
        return None

    def findDescription(self, description) -> str:
        """ Parses description in readable format, return description"""

        text = description
        indexOfTextBeginning = description.find(">")
        while indexOfTextBeginning != -1:
            if indexOfTextBeginning != len(description):
                if description[indexOfTextBeginning + 1] != "<":
                    text = description[indexOfTextBeginning + 1:]
                    text = text[: text.find('<')]
                    break
            description = description[indexOfTextBeginning + 1:]
            indexOfTextBeginning = description.find(">")
        return text

    def printingNews(self, thefeed):
        """ Prints news"""

        print("Feed: " + thefeed.feed.get("title", ""))
        print("__________________________________________________________________")

        for index, thefeedentry in enumerate(thefeed.entries):
            if (index < self.limit) | (self.limit == -1):
                listOfTags = self.takingInformationFromFeedparser(thefeedentry)

                print("Title: " + listOfTags[0])
                print("Date: " + listOfTags[1])
                print("Link: " + listOfTags[2])

                print()
                if len(listOfTags) > 4:
                    print("[image: ", listOfTags[5], "][2]", listOfTags[3])
                else:
                    print(listOfTags[3])

                print("\nLinks:")
                print("[1]:", listOfTags[2])
                linkOfImg = ""
                if len(listOfTags) > 4:
                    print("[2]:", listOfTags[4])
                    linkOfImg = listOfTags[4]
                print("__________________________________________________________________")
                putIntoDB(self.url, listOfTags[0], thefeedentry.get("published_parsed", thefeed.feed.published_parsed),
                          listOfTags[3], listOfTags[2], linkOfImg)
        return None

    def takingInformationFromFeedparser(self, thefeedentry) -> list:
        """ Creates a list with arguments: title, date, link, description, link of image and description of image, if they exist
            for each news"""

        listOfArgs = []
        listOfArgs.append(thefeedentry.get("title", ""))
        listOfArgs.append(thefeedentry.get("published", ""))
        listOfArgs.append(thefeedentry.get("link", ""))
        description = thefeedentry.get("description", "")
        text = self.findDescription(description)
        listOfArgs.append(text)

        # trying to get link of image and description of image
        indexOfLink = description.find("img src")
        linkOfImg = ""
        if indexOfLink != -1:
            linkOfImg = description[indexOfLink + 9:]
            linkOfImg = linkOfImg[: linkOfImg.find('"')]

            indexOfLink = description.find("alt")
            altOfImg = description[indexOfLink + 5:]
            altOfImg = altOfImg[: altOfImg.find('"')]

        # if link of image and description of image exists, puts them into list
        if (linkOfImg != "") | (indexOfLink != -1):
            listOfArgs.append(linkOfImg)
            listOfArgs.append(altOfImg)
        return listOfArgs

    def parseToJsonFormat(self, thefeed):
        """ Converts to json format and prints"""

        listToJson = []
        for index, thefeedentry in enumerate(thefeed.entries):
            if (index < self.limit) | (self.limit == -1):
                listOfTags = self.takingInformationFromFeedparser(thefeedentry)

                if len(listOfTags) > 4:
                    descriptionForDict = "[image: " + listOfTags[5] + "][2]" + listOfTags[3]
                    dictionary = {"Feed": thefeed.feed.get("title", ""),
                                  "Title": listOfTags[0],
                                  "Date": listOfTags[1], "Description": descriptionForDict,
                                  "Link [1]": listOfTags[2], "Link [2]": listOfTags[4]}
                    linkOfImg = listOfTags[4]
                else:
                    descriptionForDict = listOfTags[3]
                    dictionary = {"Feed": thefeed.feed.get("title", ""),
                                  "Title": listOfTags[0],
                                  "Date": listOfTags[1],
                                  "Description": descriptionForDict, "Link [1]": listOfTags[2]}
                    linkOfImg = ""
                listToJson.append(dictionary)
                putIntoDB(self.url, listOfTags[0], thefeedentry.get("published_parsed", thefeed.feed.published_parsed),
                          listOfTags[3], listOfTags[2], linkOfImg)

        # converts to json
        jsonData = json.dumps(listToJson, indent=5, ensure_ascii=False)
        print(jsonData)
        return None

    def parse(self):
        """ Parses news"""

        thefeed = feedparser.parse(self.url)
        if thefeed.get('bozo') == 1:
            stringException = thefeed.get('bozo_exception')
            logging.error(stringException)
            print(stringException)
            return None

        logging.debug("Parsing from website was successful")
        if self.jsonFormat:
            self.parseToJsonFormat(thefeed)
        elif self.to_html:
            self.convertIntoHtmlFormat(thefeed)
        else:
            self.printingNews(thefeed)
        return None
