from contextlib import closing
from urllib.error import URLError
import psycopg2
import database
import pars_args
import parser_rss
import logging
import sys


def main():
    """
        The main entry point of the application
    """
    try:
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
        with closing( database.connect_to_database()) as con:
            with con.cursor() as cursor:
                database.create_table(con, cursor)
                args = pars_args.get_args()
                list_of_news = []
                if args.date:
                    date = parser_rss.valid_date(args.date)
                    database.read_news(list_of_news, args.limit, args.source, date, cursor)
                else:
                    news_feed = parser_rss.get_news_feed(args.source)
                    parser_rss.init_list_of_news(list_of_news, news_feed, args.limit)
                    database.write_to(list_of_news, args.source, cursor)
                if args.json:
                    parser_rss.print_news_in_json(list_of_news)
                else:
                    parser_rss.print_news(list_of_news)

                con.commit()

    except psycopg2.OperationalError:
        parser_rss.print_news_without_cashing()
        print("Check your database,"
              "news is not saved "
              "you cannot use --date\n"
              "Please read README.md")
    except parser_rss.TimeOutExeption as e:
        print(e)
    except URLError as er:
        print(er)
    except ValueError as v:
        print(v)
    except FileNotFoundError as e:
        print(e)


if __name__ == '__main__':
    main()
