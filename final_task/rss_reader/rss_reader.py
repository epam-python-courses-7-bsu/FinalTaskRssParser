import logging
import sqlite3
import sys
from contextlib import closing

import converter
import database
import pars_args
import parser_rss
import print_functions


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

        with closing(database.connect_to_database('database.db')) as con:
            if args.clear:
                database.clear_the_history(con, 'database.db', 'NEWS')
            else:
                cursor = con.cursor()
                database.create_table(con, cursor, 'database.db')
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
                    if args.colorize:
                        print_functions.print_news_in_json_in_multi_colored_format(list_of_news)
                    else:
                        print_functions.print_news_in_json(list_of_news)
                else:
                    if args.colorize:
                        print_functions.print_news_in_multi_colored_format(list_of_news)
                    else:
                        print_functions.print_news(list_of_news)
                if args.to_html:
                    converter.conversion_of_news_in_html(args.to_html, list_of_news)
                if args.to_pdf:
                    converter.conversion_of_news_in_pdf(args.to_pdf, list_of_news)
                con.commit()
    except (sqlite3.OperationalError, MemoryError)as er:
        print_functions.print_news_without_cashing()
        print("Check your database,"
              "news is not saved "
              "you cannot use --date\n"
              )
        print(er)
    except parser_rss.TimeOutExeption as e:
        print(e)
    except Exception as e:
        print(e)
    except KeyboardInterrupt as key_error:
        print("The program is interrupted " + str(key_error))


if __name__ == '__main__':
    main()
