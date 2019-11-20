import feedparser
import json
import logging
import psycopg2
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

    def __init__(self, parametrUrl, parametrLimit, parametrJsonFormat = False, parametrDate = None):
        """ Inits arguments"""

        self.url = parametrUrl
        self.limit = parametrLimit
        self.jsonFormat = parametrJsonFormat
        self.date = parametrDate
        logging.debug("Check in parser")

        if self.date != None:
            self.printCashe()
        else:
            self.parse()


    def printCashe(self):
        """ Prints news from database from the specified day."""

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
            if self.limit > 0:
                cur.execute("SELECT * from cache WHERE feed = %s AND date = %s LIMIT %s",
                            (self.url, self.date, str(self.limit)))
            else:
                cur.execute("SELECT * from cache WHERE feed = %s AND date = %s", (self.url, self.date))

            rows = cur.fetchall()
            if not rows:
                print("No results\nTry to enter another date or url")
            if self.jsonFormat:
                listToJsonFormat = []
                for row in rows:
                    if row[4][1]:
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
            else:
                for row in rows:
                    print("Title: ", row[1])
                    print("Date: ", row[2])
                    print("Link: ", row[4][0])

                    print()
                    print("Description: " + row[3])

                    print("\nLinks:")
                    print("[1]:", row[4][0])
                    if row[4][1]:
                        print("[2]:", row[4][1])
                    print("__________________________________________________________________")
        except (Exception, psycopg2.DatabaseError) as error:
            logging.error(error)
        finally:
            if con is not None:
                con.close()
        return None

    def findDescription(self, description) -> str:
        """ Parses description in readable format, return description"""

        text = description
        indexOfTextBeginning = description.find(">")
        while indexOfTextBeginning != -1:
            if (description[indexOfTextBeginning + 1] != "<") & (indexOfTextBeginning != len(description)):
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
                if len(listOfTags) > 3:
                    print("[image: ", listOfTags[5], "][2]", listOfTags[3])
                else:
                    print(listOfTags[3])

                print("\nLinks:")
                print("[1]:", listOfTags[2])
                linkOfImg = ""
                if len(listOfTags) > 3:
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

                if (len(listOfTags) > 3):
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
        else:
            self.printingNews(thefeed)
        return None
