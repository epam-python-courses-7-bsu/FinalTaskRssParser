from urllib.error import URLError
import pars_args
import parser_rss
import logging
import sys
from News import News
from dateutil import parser

def main():
    """
        The main entry point of the application
    """
    args = pars_args.get_args()
    logger = logging.getLogger("rss_reader")
    logger.setLevel(logging.INFO)
    # create the logging file handler
    if not args.verbose:
        fh = logging.FileHandler("new_snake.log")
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        fh.setFormatter(formatter)
        logger.addHandler(fh)
    else:
        fh = logging.basicConfig(stream=sys.stdout,
                                 filemode='a',
                                 format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                                 datefmt='%H:%M:%S',
                                 level=logging.DEBUG)

    # add handler to logger object

    logger.info("Program started")

    list_of_news = []
    news_feed = parser_rss.get_news_feed(args.source)
    parser_rss.init_list_of_news(list_of_news, news_feed, args.limit)
    item = News(feed="feed",
                     title="title",
                     date=parser.parse("2019-11-17 10:44:20-05:00"),
                     link="link",
                     info_about_image="info_about_image",
                     briefly_about_news="briefly_about_news",
                     links_from_news=["link", "link_on_image"]
                     )
    if args.json:
        parser_rss.print_news_in_json([item,])
    else:
        parser_rss.print_news(list_of_news)


if __name__ == '__main__':
    try:
        main()
    except parser_rss.TimeOutExeption as e:
        print(e)
    except URLError as er:
        print(er)
    except ValueError as v:
        print(v)
