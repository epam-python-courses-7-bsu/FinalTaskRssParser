import logging
from string_operations import make_string_readable
import exceptions as ex
from pprint import pprint
import article
import shelve
import check_func as check

class Feed:
    """Feed class, contain feed info and list of articles """
    def __init__(self, parsed, args):
        """create feed with fixed number of articles """
        logging.info('Started creting feed')

        articles_list = []
        cashed_news_number = 0
        if args.date:
            logging.info('Started extracting data from cash')
            self.link = args.source
            self.feed_name = 'Feeds from {}'.format(args.source)
            with shelve.open('cashed_feeds') as database:
                if not database:
                    raise ex.EmptyDataBase('Local feed storage is empty')
                for date in database:
                    if args.date in date and database[date].feed_link == args.source:
                        articles_list.append(database[date])
                        cashed_news_number += 1
            if cashed_news_number == 0:
                raise ex.DateNotInDatabase('There is no feeds with this date and source in local storage')

            
            if args.limit:
                if args.limit > cashed_news_number:
                    print('Only {} feeds cashed'.format(cashed_news_number))
                    number_of_articles = cashed_news_number
                else:
                    number_of_articles = args.limit
                articles_list = articles_list[:number_of_articles]
        

        else:
            if args.limit:
                if args.limit > len(parsed.entries):
                    print('Only {} feeds avaliable'.format(len(parsed.entries)))
                    number_of_articles = len(parsed.entries)
                else:
                    number_of_articles = args.limit
            else:
                number_of_articles = len(parsed.entries)
            for i in range(number_of_articles):
                articles_list.append(article.Article(parsed.entries[i], args.source))

            self.feed_name = make_string_readable(parsed.feed.title)
            self.link = parsed.feed.link
        self.articles = articles_list

    def print_readable_feed(self):
        """print feed to stdout in readable format"""
        logging.info('Started printing feed')
        print('.' * 79)
        print('\n\n{self.feed_name}\n\n')
        print(self.link)
        for article_number, article_ in enumerate(self.articles):
            article_.print_readable_article()
        logging.info('Finished printing feed')

    def print_json_feed(self):
        """print feed to stdout in json"""
        json = {}
        for i, article_ in enumerate(self.articles):
            name = "Article {}".format(i + 1)
            json[name] = article_.make_article_json()
        json['Feed'] = self.feed_name
        json['Link'] = self.link
        pprint(json)


    def save_feed_to_database(self):
        logging.info('Saving feed to database')
        with shelve.open('cashed_feeds') as database:
            for article in self.articles:
                year = article.published.tm_year
                mon = article.published.tm_mon
                day = article.published.tm_mday
                hour = article.published.tm_hour
                minute = article.published.tm_min
                sec = article.published.tm_sec
                
                date = f'{year}{mon}{day} {hour}:{minute}:{sec}'
                if date not in database:
                    database[date] = article
        logging.info('feed saved')

